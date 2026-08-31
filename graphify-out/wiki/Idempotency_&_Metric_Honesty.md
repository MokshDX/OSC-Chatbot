# Idempotency & Metric Honesty

> 7 nodes

## Key Concepts

- **fact_match** (6 connections) — `docs/engineering/architecture/evaluation.md`
- **Where the Architecture Is Weakest** (3 connections) — `docs/engineering/architecture/overview.md`
- **OrderProcessingDraft (Prisma idempotency model)** (2 connections) — `docs/company/schema/schema-6.md`
- **IDEMPOTENCY_WINDOW_MS (15 min draft reuse)** (2 connections) — `docs/company/schema/schema-6.md`
- **An Absent Metric Is Not a Zero Metric** (2 connections) — `docs/engineering/architecture/evaluation.md`
- **Testing Known Gaps** (2 connections) — `docs/engineering/architecture/testing.md`
- **Memory Does Not Survive a Restart** (2 connections) — `docs/engineering/decisions/0013-ephemeral-session-memory.md`

## Relationships

- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (2 shared connections)
- [CartDiscount & DraftOrder Schemas](CartDiscount_%26_DraftOrder_Schemas.md) (1 shared connections)
- [Tier Pricing Metafield Keys](Tier_Pricing_Metafield_Keys.md) (1 shared connections)
- [Customer Registration Schemas](Customer_Registration_Schemas.md) (1 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (1 shared connections)
- [Anthropic Adapter](Anthropic_Adapter.md) (1 shared connections)

## Source Files

- `docs/company/schema/schema-6.md`
- `docs/engineering/architecture/evaluation.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/testing.md`
- `docs/engineering/decisions/0013-ephemeral-session-memory.md`

## Audit Trail

- EXTRACTED: 16 (84%)
- INFERRED: 3 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*