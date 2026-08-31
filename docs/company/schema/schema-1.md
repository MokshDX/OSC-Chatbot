# AutoOrderTag — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner           | Namespace | Key             | Type                                | Notes                              |
| -------------------- | --------- | --------------- | ----------------------------------- | ---------------------------------- |
| Shop                 | `oscpB2B` | `autoTagStatus` | boolean / string                    | Toggle for automatic order tagging |
| Product (definition) | `oscpB2B` | `warehouse`     | single_line_text_field (definition) | Warehouse tag metafield definition |
| Product (definition) | `oscpB2B` | `brand`         | single_line_text_field (definition) | Brand tag metafield definition     |

## Sample data

### `oscpB2B.autoTagStatus`

```json
true
```

Stored as a shop metafield value (boolean / string `"true"` / `"false"` depending on write path).

### Product metafield definitions (`oscpB2B.warehouse` / `oscpB2B.brand`)

Definitions are created/pinned via Admin GraphQL; runtime product values are free-form strings used as order tags. Example definition metadata returned to the UI:

```json
{
  "id": "gid://shopify/MetafieldDefinition/123",
  "name": "Warehouse",
  "key": "warehouse",
  "namespace": "oscpB2B",
  "description": "Warehouse code applied as an order tag"
}
```

## Notes

- Product definitions drive which product metafield values are copied onto orders when auto-tagging is enabled.
- Enabling a plan unlocks the UI but does not auto-set `autoTagStatus` to true.
