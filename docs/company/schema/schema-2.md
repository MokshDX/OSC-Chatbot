# BulkImportExport — Schema

Persistence schemas for this module. Architecture, routes, tabs, and sample CSV download UX stay in [README.md](./README.md).

## Inventory

| Data owner     | Namespace | Key         | Type   | Notes                                                                          |
| -------------- | --------- | ----------- | ------ | ------------------------------------------------------------------------------ |
| ProductVariant | `oscp`    | `priceRule` | `json` | Variant quantity-break / currency tier rules (shared with VariantTierPricing). |
| Product        | `oscp`    | `rules`     | `json` | Product-level mirror rules (shared with ProductTierPricing).                   |
| ProductVariant | `oscp`    | `rangeRule` | `json` | Date-range / campaign tier rules (Platinum Date Range Rules tab).              |

Legacy public `oscp` namespace — shared with tier-pricing Shopify Functions. This module does not own a separate schema; it bulk-reads/writes the same keys as the pricing modules.

## Sample data

### `oscp.priceRule`

```json
[
  { "q": "5", "t": "p", "v": "10", "c": "all", "cu": "USD" },
  { "q": "20", "t": "f", "v": "8.50", "c": "wholesale", "cu": "USD" }
]
```

### `oscp.rules` (product)

```json
{
  "m": "c",
  "qd": [
    { "c": "all", "mq": "2", "t": "p", "sd": "10" },
    { "c": "all", "mq": "10", "t": "f", "sd": "7.99" }
  ]
}
```

### `oscp.rangeRule`

```json
[
  {
    "q": "5",
    "t": "p",
    "v": "15",
    "c": "all",
    "s": "2026-01-01",
    "e": "2026-12-31"
  }
]
```

_(Exact date-range object fields follow the VariantTierPricing / import manager shape — keep CSV columns in sync with `utils/sampleTemplates.ts`.)_

## Notes

- **CSV templates** are not metafields. Browser downloads via `utils/sampleTemplates.ts` (Blob — no API). Keep that module in sync with `public/`:
  - `productVariant_sample_template.csv`
  - `product_sample_template.csv`
  - `activeDates_sample_template.csv`
  - `sampleCSV-template-BulkDelete-VariantRules.csv`
  - `productVariant_currency_sample_template.csv`
- Sample CSV section and tab UX remain documented in [README.md](./README.md).
