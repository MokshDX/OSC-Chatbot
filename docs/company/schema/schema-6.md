# DraftOrderProcessing — Schema

Persistence schemas for this module. Full flow, limitations, and engine narrative stay in the module root [README.md](../README.md). Architecture overview: [README.md](./README.md).

## Inventory

### Owned — mode metafields (Shop)

| Data owner | Namespace | Key                     | Type               | Notes                                                                                                                                                    |
| ---------- | --------- | ----------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shop       | `oscp`    | `orderProcessingMode`   | `single_line_text` | `"shopify_function"` (default) or `"draft_order"`. Merchant-set (GlobalSetting UI).                                                                      |
| Shop       | `oscp`    | `orderProcessingActive` | `boolean` / string | `"true"` only when mode is `draft_order` **and** plan includes the feature. Real metafield (not derived) — `cart-checkout-validation` Function reads it. |

### Owned — Prisma

| Model                  | Purpose                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `OrderProcessingDraft` | Idempotency: one row per `(shop, cartTokenHash)`; reused within `IDEMPOTENCY_WINDOW_MS` (15 min). |

```prisma
model OrderProcessingDraft {
  id            Int      @id @default(autoincrement())
  shop          String
  cartTokenHash String
  draftOrderId  String
  invoiceUrl    String
  status        String   @default("OPEN")
  createdAt     DateTime @default(now())

  @@unique([shop, cartTokenHash])
  @@index([createdAt])
  @@index([status])
}
```

Draft orders are also tagged `oscp-order-processing` in Shopify.

### Read dependency keys (other modules — not owned)

| Data owner     | Namespace | Key                | Used by                                |
| -------------- | --------- | ------------------ | -------------------------------------- |
| ProductVariant | `oscp`    | `priceRule`        | Tier / Phase-1 engine                  |
| ProductVariant | `oscp`    | `rules`            | Legacy variant rules alias             |
| ProductVariant | `oscp`    | `rangeRule`        | RangeRulesEvaluator                    |
| ProductVariant | `oscp`    | `offer_exclusions` | Offer exclusion check                  |
| Product        | `oscp`    | `rules`            | QuantityBreak / QuantityClubbed (`qd`) |
| Product        | `oscp`    | `offer_exclusions` | Offer exclusion check                  |
| Shop           | `oscp`    | `customPrice`      | OfferEvaluator / MarketOfferEvaluator  |
| Shop           | `oscp`    | `aCR`              | AdvancedCollectionsEvaluator           |
| Shop           | `oscp`    | `cartRules`        | Cart-discount coordinator              |
| Shop           | `oscp`    | `qPS`              | Clubbed vs per-product qty mode        |
| Shop           | `oscp`    | `mS`               | Market-mode gate for offers            |
| Shop           | `oscp`    | `campaignSettings` | `enableRangeRules`                     |
| Shop           | `oscp`    | `advancedOffers`   | Exclusion gating                       |
| Shop           | `oscp`    | `curConv`          | Currency conversion toggle             |

See root README Phase 2 engine table for evaluator ↔ rule source mapping.

## Sample data

### `oscp.orderProcessingMode`

```text
draft_order
```

### `oscp.orderProcessingActive`

```text
true
```

### `OrderProcessingDraft` (row shape)

```json
{
  "id": 1,
  "shop": "example.myshopify.com",
  "cartTokenHash": "a1b2c3…",
  "draftOrderId": "gid://shopify/DraftOrder/123",
  "invoiceUrl": "https://example.myshopify.com/…/invoices/…",
  "status": "OPEN",
  "createdAt": "2026-08-12T08:00:00.000Z"
}
```

## Notes

- Mode UI lives in **GlobalSetting**; this module reads/writes mode+active via `ModeService` / DiscountNode activation.
- PriceAddon (`oscp.adt`) lines are **skipped** by qty/range engines; DO mode does not fully support Add-Ons Tier Pricing (see root README).
- Cart-level `offerType: "cart"` discounts are **not** baked into draft line prices — see root README § Cart discount.
