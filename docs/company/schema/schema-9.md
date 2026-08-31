# FreeGift — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner                | Namespace        | Key                        | Type                        | Notes                                                      |
| ------------------------- | ---------------- | -------------------------- | --------------------------- | ---------------------------------------------------------- |
| Metaobject                | `oscp_freegifts` | _(fields below)_           | metaobject                  | One entry = one free-gift rule. `storefront: PUBLIC_READ`. |
| Shop                      | `oscp`           | `freegift_global_settings` | `json`                      | Progress bar / PDP / popup widget copy + colors.           |
| Shop                      | `oscp`           | `isAdvancedPlan`           | `boolean`                   | Synced from Platinum / `freeGift` via FEATURES_UPDATED.    |
| Product                   | `free_gift`      | `rules`                    | `list.metaobject_reference` | References `oscp_freegifts` entries.                       |
| DiscountAutomaticApp node | `oscp`           | `registerdTag`             | `json`                      | Aggregated customer tags for the Function.                 |

Function handle: `free-gift-discount` (`SHOPIFY_FREE_GIFT_DISCOUNT_ID`).

### Metaobject fields (`oscp_freegifts`)

| Field key              | Type                     | Notes                                                 |
| ---------------------- | ------------------------ | ----------------------------------------------------- |
| `title`                | `single_line_text_field` | Display name                                          |
| `status`               | `boolean`                | Active / inactive                                     |
| `priority`             | `number_integer`         | Rule priority                                         |
| `applies_to`           | `json`                   | `{ target, targetIds, exclude, expandedProductIds? }` |
| `customer`             | `single_line_text_field` | Eligibility (`all` / `loggedIn` / tagged)             |
| `free_gifts`           | `json`                   | Gift mode, distribution, goals                        |
| `template`             | `json`                   | Template UI cache                                     |
| `re_add_if_removed`    | `boolean`                | Re-add gift if removed from cart                      |
| `remove_if_below_tier` | `boolean`                | Remove gift when below tier                           |
| `application_method`   | `single_line_text_field` | Application method                                    |
| `is_stackable`         | `boolean`                | Stack with other rules                                |

## Sample data

### Metaobject `oscp_freegifts` (field values)

```json
{
  "title": "Spend $50 get free sample",
  "status": true,
  "priority": 1,
  "customer": "all",
  "is_stackable": false,
  "re_add_if_removed": true,
  "remove_if_below_tier": true,
  "applies_to": {
    "target": "all_products",
    "targetIds": [],
    "exclude": []
  },
  "free_gifts": {
    "gift_mode": "AUTO_ADD_SINGLE",
    "distribution_strategy": "GOAL_MET",
    "customers_get_gift_every_goal": false,
    "goals": [
      {
        "requirement_type": "cart_value",
        "minimum_value": 50,
        "free_gift": {
          "product_id": "gid://shopify/Product/111",
          "variant_id": "gid://shopify/ProductVariant/222"
        }
      }
    ]
  }
}
```

### `oscp.freegift_global_settings`

```json
{
  "progressText": "Add {{amount}} more to unlock a free gift",
  "successText": "You've unlocked a free gift!",
  "primaryColor": "#008060",
  "backgroundColor": "#F6F6F7",
  "textColor": "#202223",
  "pdpTitle": "Free gift available",
  "popupTitle": "Congratulations!",
  "popupButtonText": "Continue shopping"
}
```

### `oscp.registerdTag`

```json
{
  "tags": ["wholesale", "vip"]
}
```

## Notes

- **INV-9 exception:** standard (public) metafields — Functions cannot read private metafields.
- Domain types: `FreeGiftData`, `GlobalSettings` in `contracts/freeGift.contract.ts`.
