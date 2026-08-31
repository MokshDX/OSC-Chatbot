# AccessLock — Schema

Persistence schemas for this module. Architecture, Liquid gate injection, and membership narrative stay in [README.md](./README.md).

## Inventory

| Data owner                            | Namespace               | Key              | Type       | Notes                                                                       |
| ------------------------------------- | ----------------------- | ---------------- | ---------- | --------------------------------------------------------------------------- |
| Metaobject                            | `$app:access_lock_rule` | _(fields below)_ | metaobject | One entry = one lock rule. Admin `MERCHANT_READ`, storefront `PUBLIC_READ`. |
| Shop                                  | `oscp`                  | `appEnabled`     | `boolean`  | Mirror — feature / app active for the theme gate.                           |
| Shop                                  | `oscp`                  | `gateInstalled`  | `boolean`  | Mirror — at least one theme has the gate injected.                          |
| Discount / validation node (optional) | `oscp`                  | `lockTags`       | `json`     | Checkout hard-lock tags when `SHOPIFY_ACCESS_LOCK_VALIDATION_ID` is set.    |

### Metaobject fields (`$app:access_lock_rule`)

| Field key           | Type                     | Notes                                             |
| ------------------- | ------------------------ | ------------------------------------------------- |
| `status`            | `boolean`                | Active / inactive                                 |
| `title`             | `single_line_text_field` | Display name (max 200)                            |
| `userAccessibility` | `single_line_text_field` | `all` / `loggedin` / `specific`                   |
| `userTags`          | `json`                   | Customer tags when `userAccessibility = specific` |
| `condition`         | `json`                   | Array of `{ entity, field, operator, value }`     |

Legacy installs may still use abbreviated keys (`st` / `ti` / `ua` / `ut` / `con`) — field keys are immutable once created. See README Persistence for Liquid type resolution (`app--{numericAppId}--access_lock_rule`).

## Sample data

### Metaobject `$app:access_lock_rule` (field values)

```json
{
  "status": true,
  "title": "Wholesale catalog lock",
  "userAccessibility": "specific",
  "userTags": ["wholesale", "b2b"],
  "condition": [
    {
      "entity": "product",
      "field": "id",
      "operator": "in",
      "value": ["111", "222"]
    },
    {
      "entity": "collection",
      "field": "id",
      "operator": "in",
      "value": ["333"]
    }
  ]
}
```

### `oscp.appEnabled` / `oscp.gateInstalled`

```json
true
```

### `oscp.lockTags` (optional)

```json
{
  "tags": ["wholesale", "b2b"]
}
```

## Notes

- Domain types: `LockRule` / `AccessLockRule` / `LockCondition` in `contracts/accessLock.contract.ts`.
- Definition provisioned by `accessLockSetup.service.ts` (install hook + lazy create).
- Collection membership is resolved live in Liquid at render time — not pre-expanded at save (see README).
