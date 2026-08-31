# CustomerSegment — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner       | Namespace      | Key                   | Type                            | Notes                                         |
| ---------------- | -------------- | --------------------- | ------------------------------- | --------------------------------------------- |
| App installation | `app_settings` | `registractionForm`   | json                            | Segment / registration form JSON (shared key) |
| Customer         | `segment`      | `assigned`            | single_line_text_field / string | Segment handle                                |
| Customer         | `segment`      | `status`              | single_line_text_field / string | `approved` \| `pending`                       |
| App installation | `app_settings` | `approveNewCustomers` | string                          | Default status for new assignments            |

## Sample data

### `app_settings.registractionForm`

```json
[
  {
    "pageHeading": "Become a wholesale",
    "handle": "become-a-wholesale",
    "description": "Wholesale group",
    "form": [],
    "customers": [
      {
        "id": "gid://shopify/Customer/1",
        "firstName": "Ada",
        "lastName": "Lovelace",
        "email": "ada@example.com",
        "status": "approved",
        "rowAction": ""
      }
    ],
    "totalCount": 1
  }
]
```

### `segment.assigned`

```json
"become-a-wholesale"
```

### `segment.status`

```json
"approved"
```

### `app_settings.approveNewCustomers`

```json
"true"
```

## Notes

- `registractionForm` and `approveNewCustomers` are shared with **CustomerRegistration** (INV-9 shared-key ownership).
- Customer metafields `segment.assigned` / `segment.status` are written when assigning or approving members.
