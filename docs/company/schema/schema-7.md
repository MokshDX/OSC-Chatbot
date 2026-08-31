# EmailConfiguration — Schema

Persistence schemas for this module. Architecture, routes, and events stay in [README.md](./README.md).

## Inventory

| Data owner       | Namespace      | Key             | Type | Notes                                                 |
| ---------------- | -------------- | --------------- | ---- | ----------------------------------------------------- |
| App installation | `app_settings` | `notifications` | json | SMTP notification templates + configured from-address |

## Sample data

### `app_settings.notifications`

```json
{
  "configuerdEmailId": "merchant@example.com",
  "notifications": [
    {
      "title": "Send Customer's Approval Notification",
      "status": true,
      "subject": "Your account is approved",
      "template": "<p>[customerFirstName] [customerLastName] Your account is approved.</p>"
    },
    {
      "title": "Send Customer's Request Submitted Notification",
      "status": true,
      "subject": " Your account is under review",
      "template": "<p>[customerFirstName] [customerLastName] Your account registration is under review!</p>"
    },
    {
      "title": "Send Owner's Request Received Notification",
      "status": true,
      "subject": "A potential customer signed up",
      "template": "<p>A potential customer has submitted their details through the registration form</p>"
    },
    {
      "title": "Send OSCP Tier Pricing Rule CSV Export Notification",
      "status": true,
      "subject": "Your OSCP Tier Pricing Rule CSV Export is complete!",
      "template": "<p>Hello!</p><p><b>The OSCP Tier Pricing Rule CSV Export has been successfully completed.</b></p>"
    }
  ]
}
```

Shape: `{ configuerdEmailId, notifications: [{ title, status, subject, template }] }` — legacy `configuerdEmailId` spelling preserved.

## Notes

- Defaults match `utils/formSkeleton.ts` / `DEFAULT_EMAIL_CONFIGURATION`.
- Transport uses SMTP env vars; metafield only stores templates and the configured email id.
