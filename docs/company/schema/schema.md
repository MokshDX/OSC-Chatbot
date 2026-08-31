# AddOnsTierPricing — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner       | Namespace | Key               | Type               | Notes                                                                                       |
| ---------------- | --------- | ----------------- | ------------------ | ------------------------------------------------------------------------------------------- |
| ProductVariant   | `oscp`    | `adt`             | `json`             | One `PriceAddonData` payload per variant (status, name, template, tiers, margin overrides). |
| Shop             | `oscp`    | `cartTransformId` | `single_line_text` | Cached CartTransform GID after function registration.                                       |
| Shop (read-only) | `oscp`    | `tc`              | `json`             | Template catalogue — owned by Template; this module reads only.                             |

Storage keys match the reference PriceAddons module so `extensions/cart-transformer` keeps working.

## Sample data

### `oscp.adt`

```json
{
  "ds": "1",
  "m": "Gift wrap",
  "tpl": "T-Shirt",
  "mrgR": [{ "on": "cost", "pri": "10", "val": "2" }],
  "r": [
    {
      "mn": "1",
      "mx": "5",
      "prm": [{ "pt": "color", "v": "Red" }]
    },
    {
      "mn": "6",
      "mx": "20",
      "prm": [{ "pt": "color", "v": "Blue" }]
    }
  ]
}
```

### `oscp.cartTransformId`

```json
"gid://shopify/CartTransform/123456789"
```

_(Stored as a string value; example shows the GID shape.)_

## Notes

- Domain type: `PriceAddonData` / `PriceAddonRule` / `MarginRule` in `contracts/addOnsTierPricing.contract.ts`.
- Shape must stay compatible with `extensions/cart-transformer`.
- INV-9: intentional public `oscp` metafields shared with the deployed Function.
