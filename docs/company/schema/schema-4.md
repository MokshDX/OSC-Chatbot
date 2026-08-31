# CustomerRegistration — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner       | Namespace      | Key                   | Type   | Notes                                            |
| ---------------- | -------------- | --------------------- | ------ | ------------------------------------------------ |
| App installation | `app_settings` | `registractionForm`   | json   | Forms array (legacy key typo preserved)          |
| App installation | `oscp`         | `discountNodeId`      | string | Cached wholesale discount node GID               |
| Discount node    | `oscp`         | `isMember`            | json   | `variant_level_tags` = registration form handles |
| App installation | `app_settings` | `approveNewCustomers` | string | `"true"` → auto-approve new customers            |

## Sample data

### `app_settings.registractionForm`

```json
[
  {
    "pageHeading": "Become a wholesale",
    "handle": "become-a-wholesale",
    "description": "Sign up for a wholesale account.",
    "form": [
      {
        "sectionHeading": "General details",
        "fields": [
          {
            "label": "First name",
            "value": "",
            "hint": "First name",
            "name": "first_name",
            "type": "text",
            "validation": false
          },
          {
            "label": "Email",
            "value": "email",
            "hint": "Email address",
            "name": "email",
            "type": "email",
            "validation": false
          }
        ]
      },
      {
        "sectionHeading": "Business details",
        "fields": [
          {
            "label": "Company",
            "value": "company",
            "hint": "Company name",
            "name": "company",
            "type": "text",
            "validation": false
          }
        ]
      }
    ],
    "customers": [],
    "totalCount": 0
  }
]
```

### `oscp.discountNodeId`

```json
"gid://shopify/DiscountAutomaticNode/1234567890"
```

### `oscp.isMember`

```json
{
  "variant_level_tags": ["become-a-wholesale"]
}
```

### `app_settings.approveNewCustomers`

```json
"true"
```

## Notes

- Legacy key `registractionForm` spelling is intentional (INV-9 / wholesale parity).
- Shared with **CustomerSegment** (same forms metafield) and read by tier-pricing modules via `isMember.variant_level_tags` — no cross-module imports.
