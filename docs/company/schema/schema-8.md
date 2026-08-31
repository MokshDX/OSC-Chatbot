# ExtraFee — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner | Namespace        | Key                 | Type               | Notes                                                                                                  |
| ---------- | ---------------- | ------------------- | ------------------ | ------------------------------------------------------------------------------------------------------ |
| Metaobject | `extra_fee_rule` | _(fields below)_    | metaobject         | One entry = one rule. `storefront: PUBLIC_READ`.                                                       |
| Shop       | `oscp`           | `extraFeeProductId` | `single_line_text` | GID of the shared hidden fee product.                                                                  |
| Product    | —                | `oscp-extra-fee`    | product tag        | Tags the hidden `OSCP Extra Fee` product (status DRAFT). Pickers exclude via `NOT tag:oscp-extra-fee`. |

### Metaobject fields (`extra_fee_rule`)

| Field key                       | Type                     | Notes                                              |
| ------------------------------- | ------------------------ | -------------------------------------------------- |
| `name`                          | `single_line_text_field` | Rule display name                                  |
| `status`                        | `single_line_text_field` | `"0"` / `"1"`                                      |
| `priority`                      | `number_integer`         | Evaluation order                                   |
| `customer_apply_to`             | `single_line_text_field` | `all` / `logged_in` / `customer_tags`              |
| `customer_tags`                 | `json`                   | Tags when `customer_apply_to = customer_tags`      |
| `resourceType`                  | `single_line_text_field` | Scope: all / products / variants / collections     |
| `resourceIds`                   | `json`                   | Selected resource GIDs                             |
| `resource_items`                | `json`                   | Display cache for picker items                     |
| `resource_expanded_product_ids` | `json`                   | Collection scopes expanded to product IDs on save  |
| `product_exclude_type`          | `single_line_text_field` | `none` / `specific_products` / `specific_variants` |
| `product_exclude_ids`           | `json`                   | Excluded resource GIDs                             |
| `product_exclude_items`         | `json`                   | Display cache for exclusions                       |
| `fee_calculation`               | `single_line_text_field` | `all_applied_items` / `per_item`                   |
| `fee_condition_type`            | `single_line_text_field` | `quantity` / `order_amount`                        |
| `quantity_ranges`               | `json`                   | Tier rows (`from`, `to`, `fee_type`, `fee_amount`) |
| `fee_product_id`                | `single_line_text_field` | Stamped fee product GID on the rule                |

## Sample data

### Metaobject `extra_fee_rule` (field values)

```json
{
  "name": "Packaging fee",
  "status": "1",
  "priority": 1,
  "customer_apply_to": "all",
  "customer_tags": [],
  "resourceType": "all_products",
  "resourceIds": [],
  "resource_items": [],
  "resource_expanded_product_ids": [],
  "product_exclude_type": "none",
  "product_exclude_ids": [],
  "product_exclude_items": [],
  "fee_calculation": "all_applied_items",
  "fee_condition_type": "quantity",
  "quantity_ranges": [
    {
      "from": "1",
      "to": "10",
      "fee_type": "fixed_fee",
      "fee_amount": "5.00"
    },
    {
      "from": "11",
      "to": "999",
      "fee_type": "percentage",
      "fee_amount": "2"
    }
  ],
  "fee_product_id": "gid://shopify/Product/999"
}
```

### `oscp.extraFeeProductId`

```text
gid://shopify/Product/999
```

## Notes

- Keys intentionally identical to the reference project so the theme app extension keeps working.
- Domain type: `ExtraFeeRule` in `contracts/extraFee.contract.ts`.
- Setup: `ExtraFeeSetupService.seed` ensures the metaobject definition + hidden fee product + shop metafield.
