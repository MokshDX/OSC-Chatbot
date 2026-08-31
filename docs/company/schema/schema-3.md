# CartDiscount — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner                | Namespace | Key               | Type           | Notes                                                        |
| ------------------------- | --------- | ----------------- | -------------- | ------------------------------------------------------------ |
| Shop                      | `oscp`    | `cartRules`       | `json`         | Array of `CartDiscountData` offers — the feature “database”. |
| DiscountAutomaticApp node | `oscp`    | `isCartTags`      | `json`         | Aggregated `{ tags, collections }` for Function eligibility. |
| Shop                      | `oscp`    | `cartCollections` | _(deprecated)_ | Cleaned up via `metafieldDelete` on save.                    |

A single automatic-app discount node titled **"OSCP CART DISCOUNT"** (`SHOPIFY_ORDER_DISCOUNT_ID`) backs all offers; created on first save if missing.

## Sample data

### `oscp.cartRules`

```json
[
  {
    "discountStatus": "1",
    "discountLabel": "Spend $100 get 5% off",
    "offerType": "cart",
    "offerResources": [],
    "userAccessibility": "all",
    "userTags": [],
    "offerValues": [
      {
        "offerCondition": "order-amount-value",
        "minCartValue": "100",
        "minCartQuantity": "0",
        "collections": [],
        "products": [],
        "type": "percent",
        "discountValue": "5"
      }
    ],
    "startsAt": "2026-01-01T00:00:00Z",
    "endsAt": null
  }
]
```

### `oscp.isCartTags`

```json
{
  "tags": ["wholesale", "vip"],
  "collections": ["gid://shopify/Collection/123"]
}
```

## Notes

- **INV-9 exception:** these are STANDARD (public) metafields, not `privateMetafield`, because a Shopify Function reads them as input — private metafields are not visible to Functions. The linter emits an INV-9 advisory for `metafieldsSet`; this is the sanctioned reason.
- Domain type: `CartDiscountData` in `contracts/cartDiscount.contract.ts`.
- Advanced `collections-value` / `specific-products-value` per-tier conditions are supported in the schema even when the UI only exposes order-amount / order-quantity.
