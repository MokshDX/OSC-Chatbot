# Production Deployment Runbook

Owner: Platform Engineering. Escalation: `#platform-oncall`.

## Deployment window

Production deployments are permitted **Monday to Thursday, 09:00 to 16:00 CET**.
Friday deployments are blocked by default because the on-call rotation thins over
the weekend and a Friday regression is typically discovered on Monday.

Emergency fixes may deploy outside the window with approval from the on-call
engineering manager, recorded in the incident channel.

## Pre-deployment checklist

1. All CI checks green on the release commit.
2. Database migrations reviewed by a second engineer.
3. Rollback plan written into the release ticket.
4. Feature flags for the release set to `off` in production.

## Procedure

Deployments use a blue-green strategy. The new revision is brought up alongside
the current one and receives no traffic until its health check passes.

Traffic shifts in three stages: **10 percent for 10 minutes**, then **50 percent
for 10 minutes**, then 100 percent. Error rate and p95 latency are watched at each
stage. An error rate above **2 percent** aborts the rollout automatically.

Database migrations are applied **before** the new revision receives traffic, and
must be backward compatible with the currently running revision. A migration that
cannot be made backward compatible is split across two releases.

## Rollback

Rollback is a traffic shift back to the previous revision and takes under two
minutes. It is always the first response to a production regression; diagnosis
happens after traffic is safe.

Migrations are never rolled back automatically. A forward fix is written instead,
because reversing a migration that has already accepted writes loses data.

## Post-deployment

Watch dashboards for 30 minutes after reaching 100 percent traffic. Record the
release in the deployment log with the commit SHA, the deployer and the outcome.
