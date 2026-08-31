# Graph Report - /Users/mokshdutt/Developer/OFC/chatbot  (2026-09-01)

## Corpus Check
- 10 files · ~213,898 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2651 nodes · 5469 edges · 171 communities (127 shown, 44 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 437 edges (avg confidence: 0.71)
- Token cost: 60,000 input · 0 output

## Community Hubs (Navigation)
- FastAPI Routes & Session Endpoints
- Protocol Seams & Container
- Ingestion Loaders & Parsers
- Conversational Evaluator
- Doctor Health Checks
- API Layer Tests
- Error Hierarchy
- PgVector Store
- LLM-as-Judge Faithfulness
- Provider Registration & Embeddings
- Evaluation Runner Tests
- RRF Fusion & Citation Parsing
- Regression Gate Tests
- AccessLock & BulkImportExport Schemas
- Answer & Citation Types
- PgVector SQL & Inspection
- Span Tree & Trace Core
- Answerer & Abstention Policy
- Regression Gate Engine
- OpenAI-Compatible Provider
- LangChain Integration Tests
- Document Loaders
- Trace Configuration & Rendering
- Golden Set & Case Results
- Eval CLI Command
- In-Memory Session Store
- LangChain Chat Bridge
- Memory Vector Store
- Logging Tests
- Composition Root & Settings
- Evaluation Framework Rationale
- Conversational Evaluation Tests
- Ingestion Tests
- Server Lifecycle Tests
- Logging Filters & Audit Stream
- Recursive Chunker
- Test Doubles & Stubs
- Suite Loading & Validation
- Settings Precedence Tests
- Quality Report Renderer
- Chunking & Embedding Architecture
- Anthropic Adapter
- Conversation Turn Orchestration
- Generation & Abstention Metrics
- Core CLI Commands
- Reranker & Retrieval Settings
- Session Memory Architecture
- Chunker Registration
- Persistent Trace Store Tests
- LangChain Splitters
- Gemini Adapter
- ADR 0001 Protocol Seams
- CLI Tests
- Measured Chunker Decision & IR Metrics
- Logging System Design
- StoreInspector Protocol
- VectorStore Protocol
- Evaluation Methodology & Sources
- Cross-Encoder Reranker
- Session Memory Tests
- Session Store Internals
- Evaluation Framework ADR
- Embeddings & Vector Width
- Retrieval Metric Functions
- Reasoning-Model Hygiene
- Trace Persistence
- Default Local Profile
- Observability Subsystem
- Golden Case Validators
- Fusion & Provider Packages
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82
- Community 83
- Community 84
- Community 85
- Community 86
- Community 87
- Community 88
- Community 89
- Community 90
- Community 91
- Community 92
- Community 93
- Community 94
- Community 95
- Community 96
- Community 97
- Community 98
- Community 99
- Community 100
- Community 101
- Community 102
- Community 103
- Community 104
- Community 105
- Community 106
- Community 107
- Community 108
- Community 109
- Community 110
- Community 111
- Community 112
- Community 113
- Community 114
- Community 115
- Community 116
- Community 117
- Community 118
- Community 119
- Community 120
- Community 121
- Community 122
- Community 123
- Community 124
- Community 125
- Community 126
- Community 127
- Community 128
- Community 129
- Community 130
- Community 131
- Community 132
- Community 133
- Community 134
- Community 135
- Community 136
- Community 137
- Community 138
- Community 139
- Community 140
- Community 141
- Community 142
- Community 143
- Community 144
- Community 145
- Community 146
- Community 147
- Community 148
- Community 149
- Community 150
- Community 151
- Community 152
- Community 153
- Community 154
- Community 155
- Community 156
- Community 157
- Community 158
- Community 159
- Community 160
- Community 161
- Community 162
- Community 163
- Community 164
- Community 165
- Community 166
- Community 167
- Community 169
- Community 170

## God Nodes (most connected - your core abstractions)
1. `Container` - 64 edges
2. `MemoryVectorStore` - 63 edges
3. `StubEmbeddingModel` - 59 edges
4. `ChatRequest` - 57 edges
5. `Document` - 54 edges
6. `ComponentConfig` - 49 edges
7. `InMemorySessionStore` - 46 edges
8. `PgVectorStore` - 43 edges
9. `Settings` - 37 edges
10. `ScoredChunk` - 36 edges

## Surprising Connections (you probably didn't know these)
- `FEAT-01 Quantity Break Pricing (SCN-001, SCN-002)` --semantically_similar_to--> `Add-on Tier Pricing`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_B2B_Scenario_Document-1_cb06f24b.md → docs/company/faq/add-on-tier-pricing.md
- `FEAT-04 Cart Level Discount (SCN-006, SCN-007)` --semantically_similar_to--> `Cart Discount`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_B2B_Scenario_Document-1_cb06f24b.md → docs/company/faq/cart-discount.md
- `FA-10 Manual Order Support` --semantically_similar_to--> `Draft Order Processing`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_Wholesale_B2B_Scenario_Templates_0ba70067.md → docs/company/faq/draft-order.md
- `OSC Engineering Handbook (claude.md)` --semantically_similar_to--> `OSC Engineering Handbook (AGENTS.md)`  [INFERRED] [semantically similar]
  claude.md → AGENTS.md
- `Observability Rules (claude.md)` --semantically_similar_to--> `Observability Rules for New Code`  [INFERRED] [semantically similar]
  claude.md → AGENTS.md

## Import Cycles
- 3-file cycle: `src/osc_assistant/evaluation/__init__.py -> src/osc_assistant/evaluation/conversational.py -> src/osc_assistant/evaluation/runner.py -> src/osc_assistant/evaluation/__init__.py`

## Hyperedges (group relationships)
- **The Measured Chunker Decision And Its Unresolved Consequence** — project_status_markdown_chunker_decision, docs_engineering_architecture_chunking_and_embeddings_markdown_chunker, docs_engineering_architecture_chunking_and_embeddings_recursive_chunker, docs_engineering_architecture_chunking_and_embeddings_reindex_after_chunker_change, project_status_top_k_untuned, docs_engineering_architecture_retrieval_measured_baseline [EXTRACTED 1.00]
- **The Only Path By Which Conversation History Reaches Retrieval** — project_status_session_memory, docs_engineering_architecture_retrieval_query_rewriting, docs_engineering_architecture_retrieval_follow_up_lift, project_status_cold_control, project_status_conversational_evaluation, project_status_query_rewriting_decision [EXTRACTED 1.00]
- **The Corpus Boundary Is One Setting, And It Fails Safe** — docs_engineering_architecture_knowledge_corpus_corpus_root, project_status_corpus_root_setting, docs_engineering_architecture_knowledge_corpus_company_engineering_split, docs_engineering_architecture_knowledge_corpus_schema_over_company, docs_engineering_architecture_knowledge_corpus_current_contents [EXTRACTED 1.00]
- **INV-9: public metafields because Shopify Functions cannot read private ones** — docs_company_schema_schema_3_inv9_public_metafield_exception, docs_company_schema_schema_3_oscp_iscarttags, docs_company_schema_schema_9_oscp_registerdtag, docs_company_schema_schema_oscp_adt, docs_company_schema_schema_6_orderprocessingactive [EXTRACTED 1.00]
- **Conversational memory proven by the cold-control lift measurement** — docs_engineering_architecture_conversation_query_rewriter_gap, config_default_rewrite_queries, project_status_cold_control, docs_engineering_architecture_evaluation_methodology_follow_up_lift, docs_engineering_architecture_evaluation_methodology_context_pollution [EXTRACTED 1.00]
- **A chunker change measured, gated and reindexed end to end** — config_default_chunking_markdown, config_default_chunker_comparison_table, readme_reindex_after_chunker_change, docs_engineering_architecture_evaluation_methodology_document_level_relevance, docs_engineering_architecture_evaluation_methodology_regression_gates [EXTRACTED 1.00]
- **The Derived, Self-Explaining CI Gate** — docs_engineering_decisions_0014_derived_regression_tolerances_adr, docs_engineering_decisions_0014_derived_regression_tolerances_derived_tolerances, docs_engineering_decisions_0014_derived_regression_tolerances_tradeoff_guards, docs_engineering_architecture_evaluation_ci_gate, docs_engineering_architecture_evaluation_deterministic_gate_principle, evaluation_baselines_readme_committed_baselines [EXTRACTED 1.00]
- **Ephemeral Conversational Memory, End to End** — docs_engineering_decisions_0013_ephemeral_session_memory_inmemorysessionstore, docs_engineering_decisions_0013_ephemeral_session_memory_conversation, src_osc_assistant_api_static_index_client_session_lifecycle, evaluation_suites_conversational_cold_control_run, docs_engineering_architecture_retrieval_query_rewriting [INFERRED 0.85]
- **The Four Load-Bearing Properties of the Logging System** — docs_engineering_architecture_logging_async_queue_writes, docs_engineering_architecture_logging_trace_id_correlation, docs_engineering_architecture_logging_bounded_disk_rotation, docs_engineering_architecture_logging_redaction_filter, docs_engineering_architecture_logging_logging_system [EXTRACTED 1.00]
- **The Failure Diagnosis Loop** — agents_operational_tooling, docs_engineering_architecture_observability_debugging_workflow, docs_engineering_architecture_logging_audit_stream [EXTRACTED 1.00]
- **Tier price precedence resolution across variant, product and collection scopes** — docs_company_faq_priority_of_the_offers_offer_priority, docs_company_faq_priority_of_the_offers_offer_list_ordering, docs_company_faq_tiered_pricing_guide_tiered_pricing, docs_company_faq_combined_collection_quantity_discount_slabs_best_tier_across_collections, graphify_out_converted_oscp_wholesale_b2b_scenario_templates_0ba70067_ec_01_multiple_tag_discount_conflict [INFERRED 0.85]
- **B2B account onboarding: registration, notification, approval, tag-gated pricing** — docs_company_faq_registration_form_registration_form, docs_company_faq_registration_form_email_notification_setup, graphify_out_converted_oscp_b2b_scenario_document_1_cb06f24b_feat_06_b2b_registration_form, graphify_out_converted_oscp_b2b_scenario_document_1_cb06f24b_feat_12_email_notifications, graphify_out_converted_oscp_wholesale_b2b_scenario_templates_0ba70067_fa_05_b2b_registration_form [INFERRED 0.85]
- **Delivering the wholesale price at checkout via Draft Orders** — docs_company_faq_draft_order_draft_order_processing, docs_company_faq_draft_order_server_side_price_validation, docs_company_faq_draft_order_invoice_reuse_window, docs_company_faq_draft_order_oscp_order_processing_tag, docs_company_faq_draft_order_coupon_after_tier_discount_ordering [EXTRACTED 1.00]
- **The Five Swappability Protocols** — docs_engineering_architecture_provider_architecture_chatmodel_protocol, docs_engineering_architecture_provider_architecture_embeddingmodel_protocol, docs_engineering_architecture_provider_architecture_vectorstore_protocol, docs_engineering_architecture_provider_architecture_reranker_protocol, docs_engineering_architecture_provider_architecture_chunker_protocol [EXTRACTED 1.00]
- **Enforcing The Corpus Boundary** — docs_engineering_decisions_0007_knowledge_corpus_layout_exclusion_list_rejected [INFERRED 0.95]
- **Scoped LangChain adoption: bridge providers, heading-aware splitting, the experiment profile and the citation cost it carries** — config_experiments_langchain_bridge_profile, config_experiments_langchain_bridge_markdown_chunking [INFERRED 0.85]

## Communities (171 total, 44 thin omitted)

### Community 0 - "FastAPI Routes & Session Endpoints"
Cohesion: 0.05
Nodes (59): HTMLParser, ParseError, A source file could not be turned into text. Raised per file and caught by the…, Corpus ingestion: connectors, text extraction, and the chunk/embed/store…, _derive_title(), FilesystemLoader, Path, Corpus connectors. A loader is any object with `load() ->… (+51 more)

### Community 1 - "Protocol Seams & Container"
Cohesion: 0.05
Nodes (47): PgVectorOptions, PgVectorStore, Any, BaseModel, Adapter over PostgreSQL with the pgvector extension., The partition this store reads and writes. Every query is scoped to it., Open the pool and, unless disabled, apply pending migrations., Apply unapplied migration files in filename order. A hand-rolled runner rather… (+39 more)

### Community 2 - "Ingestion Loaders & Parsers"
Cohesion: 0.07
Nodes (37): ConfigurationError, DimensionMismatchError, MissingDependencyError, Exception hierarchy for the assistant. A single root (`AssistantError`) lets…, The system is misconfigured and cannot start or serve a request. Raised for…, A component was requested by a name that is not registered., A provider was selected but its optional dependency is not installed., The configured embedding model does not match the store's vector width.… (+29 more)

### Community 3 - "Conversational Evaluator"
Cohesion: 0.07
Nodes (45): Chunking strategies. Imported for registration side effects., _build_langchain_recursive(), _build_markdown(), _heading_path(), LangChainRecursiveChunker, MarkdownChunker, Any, register (+37 more)

### Community 4 - "Doctor Health Checks"
Cohesion: 0.06
Nodes (43): Observability: tracing, persistence, and the rendering of traces. Three modules…, _details(), _label(), Rendering a trace for a human. Separate from `trace` because collection and…, Draw the trace as an indented waterfall. Bars are positioned by `offset_ms` and…, One line: id, name, duration, span count, outcome., The first few attributes, plus any error. Truncated on purpose: a waterfall is…, render_summary() (+35 more)

### Community 5 - "API Layer Tests"
Cohesion: 0.06
Nodes (53): TestClient, client(), _development_client(), _parse_sse(), Document, fixture, parametrize, HTTP layer tests. These run the real application — real container, real… (+45 more)

### Community 6 - "Error Hierarchy"
Cohesion: 0.06
Nodes (44): LangChainChunkerOptions, `ChunkerOptions` plus the settings only the LangChain splitters expose., LangChainEmbeddingModel, Vector, Catch a misconfigured `dimensions` at the first call rather than at query time.…, Adapter presenting a LangChain embeddings object as an OSC `EmbeddingModel`., LangChainChatOptions, BaseModel (+36 more)

### Community 7 - "PgVector Store"
Cohesion: 0.09
Nodes (39): ChunkerOptions, BaseModel, Splits on the coarsest separator that keeps chunks under the target size. Falls…, RecursiveChunker, InMemoryLoader, Serves a fixed list of documents. Used by tests and the evaluation harness., IngestionPipeline, Delete indexed documents that the source no longer offers. `keep` is every… (+31 more)

### Community 8 - "LLM-as-Judge Faithfulness"
Cohesion: 0.05
Nodes (42): Conversation — What a Turn Is, session_context Span, Writing Is Off the Calling Thread, The Audit Stream, Disk Bounded by Construction, Corpus Text Reduced to a Length, The cli.command Record, Configuration (+34 more)

### Community 9 - "Provider Registration & Embeddings"
Cohesion: 0.10
Nodes (42): evaluate_gate(), Compare `current` against `baseline` and decide whether it may ship. Both…, _abstention_cases(), _cases(), Any, Regression gate tests. The gate is the only part of this system that can stop a…, Six abstention cases are far noisier than forty fact cases. Giving both the…, A laptop under load is not a quality regression. (+34 more)

### Community 10 - "Evaluation Runner Tests"
Cohesion: 0.09
Nodes (28): AnswerEvent, _annotate_abstention(), _annotate_generation(), AnswerComplete, Answerer, _audit_answer(), Answer generation: the composition of retrieval and a chat model. This is the…, Answer `question`, emitting events as they become available. (+20 more)

### Community 11 - "RRF Fusion & Citation Parsing"
Cohesion: 0.06
Nodes (24): ChatModel, Chunker, EmbeddingModel, Reranker, Self, _inspector(), Container, Answerer (+16 more)

### Community 12 - "Regression Gate Tests"
Cohesion: 0.10
Nodes (37): Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…, reciprocal_rank_fusion(), parse_marker_citations(), Render sources as a delimited block for inclusion in a prompt. The delimiter…, Extract citations from `[n]` markers in `text`. Markers referring to a source…, render_sources(), A retrieved chunk presented to the model as grounding material., SourceDocument (+29 more)

### Community 13 - "AccessLock & BulkImportExport Schemas"
Cohesion: 0.08
Nodes (34): Expand one execution trace into a stage-by-stage waterfall. With no id this…, trace(), Sync `documents` into the store. Args: documents: The full current contents of…, annotate(), configure_tracing(), Install tracing configuration. Safe to call more than once., Attach attributes to the innermost active span, if there is one. The…, Process-wide tracing behaviour, set once from settings at startup. Module-level… (+26 more)

### Community 14 - "Answer & Citation Types"
Cohesion: 0.11
Nodes (25): Evaluator, Runs a golden set and scores it. Takes the pipelines rather than the…, _golden(), parametrize, RetrievalPipeline, Evaluation harness tests. The harness is the instrument every future retrieval…, Regression: `fact_match` used to read 1.0 for a run that generated nothing.…, An unreachable judge must not be scored as either faithful or unfaithful.… (+17 more)

### Community 15 - "PgVector SQL & Inspection"
Cohesion: 0.08
Nodes (35): _build_corpus(), conversation(), corpus(), indexed(), _purge(), fixture, Path, End-to-end smoke test against the real stack. Everything else in this suite… (+27 more)

### Community 16 - "Span Tree & Trace Core"
Cohesion: 0.10
Nodes (31): InMemorySessionStore, Session-scoped conversational memory. Until this module existed, every question…, Process-local conversation memory, bounded three ways. The bounds are the…, How many sessions are currently held. For `doctor` and for tests., Bounds on ephemeral conversational memory. Every value here is a ceiling, not a…, SessionSettings, Session-scoped conversational memory. The properties tested here are the ones a…, False rather than raising: the API's DELETE is idempotent by design. (+23 more)

### Community 17 - "Answerer & Abstention Policy"
Cohesion: 0.12
Nodes (34): active_trace_store(), configure_observability(), Path, Install the whole observability stack. Safe to call more than once. Persistence…, The store traces are being written to, if persistence is enabled., _isolated_tracing(), fixture, Path (+26 more)

### Community 18 - "Regression Gate Engine"
Cohesion: 0.11
Nodes (32): _assert_resolvable(), _default_baseline(), _default_output(), eval(), _execute(), _execute_conversational(), _filtered(), _plan() (+24 more)

### Community 19 - "OpenAI-Compatible Provider"
Cohesion: 0.09
Nodes (27): ConversationalCase, ConversationalTurn, Answer, Run one session end to end, closing it whichever way the case ends. The session…, Re-run this turn's question cold, and attach what it retrieved. Retrieval only.…, Aggregate turns into the conversational numbers a run is judged on. Failed…, Fraction of turns whose session held exactly its own conversation, no more.…, One scored turn. Flat and JSON-serialisable, like `CaseResult`. (+19 more)

### Community 20 - "LangChain Integration Tests"
Cohesion: 0.11
Nodes (21): ProviderError, An upstream provider (LLM, embeddings, reranker) failed., compose_grounded_system(), Fold the system prompt, citation instruction and sources into one string. Used…, StreamEvent, Generate a response incrementally., _build_contents(), _finish_reason() (+13 more)

### Community 21 - "Document Loaders"
Cohesion: 0.11
Nodes (28): ConversationalEvaluator, Runs a multi-turn golden set and scores it., GenerationSettings, corpus(), evaluator(), Document, fixture, StubEmbeddingModel (+20 more)

### Community 22 - "Trace Configuration & Rendering"
Cohesion: 0.10
Nodes (20): Chunk, ConversationalCase, ConversationalSet, ConversationalTurn, document_key(), GoldenCase, BaseModel, field_validator (+12 more)

### Community 23 - "Golden Set & Case Results"
Cohesion: 0.09
Nodes (22): Logger, Executes multi-turn golden cases against a live system and scores them.…, FaithfulnessJudge, _parse_verdict(), LLM-as-judge faithfulness scoring. Faithfulness asks whether every claim in an…, Read a one-word verdict out of whatever the model actually returned. Substring…, Scores one answer against the passages it was generated from., Return True, False, or None when the judge could not be reached. `None` rather… (+14 more)

### Community 24 - "Eval CLI Command"
Cohesion: 0.08
Nodes (20): Protocol, ChatModel, Read-only introspection of what a store currently holds. Kept **separate from…, Corpus-wide counts and chunk-size distribution., Indexed documents, newest first. `search` matches title or source URI., One document's index record, or None if it is not indexed., Every chunk of a document, in ordinal order., One chunk with its full text — what the model was actually shown. (+12 more)

### Community 25 - "In-Memory Session Store"
Cohesion: 0.15
Nodes (30): Path, Persistent logging tests. Logging is the system that gets read when something…, The seam between the two observability systems. Without this field, logs and…, The span bridge: pipeline coverage with no call site in any pipeline., A secret suppressed on disk and printed to stdout is a secret that leaked., Every JSON record in a log file, flushed and parsed., Raising our level to TRACE must not turn on every vendor SDK's firehose. Those…, _records() (+22 more)

### Community 26 - "LangChain Chat Bridge"
Cohesion: 0.11
Nodes (30): Abstention Cases in the Golden Set, Evaluation CI Gate, Deterministic Metrics Gate CI, Document-Level Relevance Scoring, LLM-as-Judge Faithfulness, Golden Set, --reindex After a Chunker Change, Golden-Set Path Guard (+22 more)

### Community 27 - "Memory Vector Store"
Cohesion: 0.07
Nodes (18): Chunk, embed and store one document. Each of the three stages gets its own…, Remove a document and every chunk belonging to it., Map document id to stored content hash, for incremental sync., Every document id currently indexed., Lexical search. Return `[]` if the store has no lexical index., Persistence and retrieval of embedded chunks. Implementations that cannot do…, Prepare the store (connect, create collections). Idempotent., The vector width this store is configured to hold. (+10 more)

### Community 28 - "Logging Tests"
Cohesion: 0.12
Nodes (21): The collected text, with each block element on its own line., _build(), _instantiate(), LangChainChatModel, _parse_usage(), Any, register, StreamEvent (+13 more)

### Community 29 - "Composition Root & Settings"
Cohesion: 0.15
Nodes (28): pipeline(), Document, fixture, IngestionPipeline, MemoryVectorStore, Path, StubEmbeddingModel, Ingestion tests. Idempotency is the property that matters: a re-run over an… (+20 more)

### Community 30 - "Evaluation Framework Rationale"
Cohesion: 0.10
Nodes (28): exploding_client(), fixture, TestClient, Startup, shutdown and in-flight failure behaviour of the service. These cover…, A condition worth interrupting a developer for belongs in the log as well., A client told nothing waits forever. The handler previously caught only…, An unexpected exception's message is not part of the API contract., `AssistantError` messages are written for operators and are safe to surface. (+20 more)

### Community 31 - "Conversational Evaluation Tests"
Cohesion: 0.09
Nodes (28): Measurement Rules, Two Canonical Commands (make verify / make eval), abstention_accuracy, A Case Never Aborts the Run, citation_coverage, citation_precision, Configuration Travels With the Numbers, Evaluation Harness (+20 more)

### Community 32 - "Ingestion Tests"
Cohesion: 0.10
Nodes (28): Chunk Denormalises Title And Source URI, Chunking And Embedding Pipeline, EmbeddedChunk Carries Its Embedding Model Id, fixed Chunking Strategy, langchain_recursive Chunking Strategy, markdown Chunking Strategy (default since ADR 0012), recursive Chunking Strategy (former default, superseded by markdown), Why Documents Are Split At All (+20 more)

### Community 33 - "Server Lifecycle Tests"
Cohesion: 0.08
Nodes (28): Shared Chunk Id Helper And Idempotent Ingestion, --reindex Required After A Chunker Change, ADR 0001 — Five Protocols As The Swappability Seams, Rejected: Abstract Base Classes And Framework Abstractions, Provider-Specific Tuning Lives In Untyped options, ADR 0002 — Adopt LangChain For Undifferentiated Work Only, langchain-core And langchain-text-splitters Are Core Dependencies, ADR 0005 — An In-Repo Evaluation Harness, Not A Third-Party One (+20 more)

### Community 34 - "Logging Filters & Audit Stream"
Cohesion: 0.15
Nodes (28): chunk(), config(), doctor(), document(), documents(), logs(), providers(), Argument (+20 more)

### Community 35 - "Recursive Chunker"
Cohesion: 0.12
Nodes (15): Generate a complete response., ChatResponse, Citation, CitationDelta, A reference from the answer back to the material that supports it. `index` is…, An incremental fragment of the answer., A citation resolved mid-stream., StreamEnd (+7 more)

### Community 36 - "Test Doubles & Stubs"
Cohesion: 0.14
Nodes (24): DocumentSummary, Check, _check_chunker(), _check_corpus(), _check_langchain(), _check_llm(), _check_reranker(), _check_store() (+16 more)

### Community 37 - "Suite Loading & Validation"
Cohesion: 0.09
Nodes (20): LogRecord, _AuditOnly, configure_logging(), _ExcludeAudit, JsonFormatter, log_directory(), _NonDestructiveQueueHandler, Path (+12 more)

### Community 38 - "Settings Precedence Tests"
Cohesion: 0.10
Nodes (18): MemoryVectorStore, A dictionary-backed `VectorStore`., Store inspection tests. `StoreInspector` is what the operational commands are…, The last step of verifying a citation: the exact text the model was shown., The protocol is optional; a store that cannot support it is still a store. Both…, The point of measuring is comparing against the configured target. A…, test_a_chunk_can_be_fetched_by_id(), test_a_deleted_document_leaves_no_trace() (+10 more)

### Community 39 - "Quality Report Renderer"
Cohesion: 0.17
Nodes (20): A deterministic bag-of-words embedder. Hashes each token into a fixed number of…, A chat model that returns a scripted reply. `supports_citations` is False, so…, StubChatModel, StubEmbeddingModel, _answerer(), Answer generation tests. The abstention policy is the system's main defence…, Both citation paths must produce the same shape for downstream code., The complete event is authoritative: clients discard streamed text when it… (+12 more)

### Community 40 - "Chunking & Embedding Architecture"
Cohesion: 0.14
Nodes (25): load_settings(), Build settings, applying `overrides` at the highest precedence., _isolate_environment(), _profile(), fixture, MonkeyPatch, Path, Configuration precedence tests. `settings.py` carries the only hand-written… (+17 more)

### Community 41 - "Anthropic Adapter"
Cohesion: 0.10
Nodes (25): session: max_messages / max_sessions / idle_ttl_seconds, InMemorySessionStore (bounded three ways), SessionStore Protocol, Structural Session Isolation (unguessable token), session_isolation metric, Abstention Is a Code Path, Not a Prompt Instruction, Instrumentation in Pipelines, Not Adapters, Business Logic Never Imports a Provider (+17 more)

### Community 42 - "Conversation Turn Orchestration"
Cohesion: 0.13
Nodes (17): AnthropicChatModel, AnthropicOptions, _build(), _build_messages(), _last_user_index(), _parse_content(), _parse_usage(), Any (+9 more)

### Community 43 - "Generation & Abstention Metrics"
Cohesion: 0.12
Nodes (25): StubChatModel, conversation(), Document, fixture, MemoryVectorStore, StubEmbeddingModel, Single-turn behaviour is unchanged by the existence of sessions., The load-bearing assertion of this whole module. Checked against what the… (+17 more)

### Community 44 - "Core CLI Commands"
Cohesion: 0.15
Nodes (22): ExplainOption, _answer_payload(), ask(), ingest(), _print_answer(), Answer, Argument, command (+14 more)

### Community 45 - "Reranker & Retrieval Settings"
Cohesion: 0.19
Nodes (22): Console, _bar(), _fact_match(), _format(), _is_bounded(), _mean(), Any, Renders an evaluation run as the quality report. Separate from `runner` and… (+14 more)

### Community 46 - "Session Memory Architecture"
Cohesion: 0.12
Nodes (17): OSCRetriever(), Any, Build a LangChain `BaseRetriever` over an OSC retrieval pipeline. A factory…, Retrieval: query rewriting, search and reranking., Dispatch to the store, timing it and recording the shape of the result. The…, Composes rewriting, search and reranking into one call., RetrievalPipeline, QueryRewriter (+9 more)

### Community 47 - "Chunker Registration"
Cohesion: 0.11
Nodes (15): Chat model providers. Imported for registration side effects., _make_factory(), OpenAICompatibleChatModel, OpenAICompatibleOptions, _parse_usage(), _Preset, Any, BaseModel (+7 more)

### Community 48 - "Persistent Trace Store Tests"
Cohesion: 0.14
Nodes (18): Citation, Run retrieval only. Exposed as its own endpoint because retrieval quality is…, search(), AnswerBody, CitationBody, HealthBody, Answer, Any (+10 more)

### Community 49 - "LangChain Splitters"
Cohesion: 0.10
Nodes (22): Lazy cached_property Container Construction, PEP 544 — Structural Subtyping, Registry And Composition Root Wiring, Protocols Rather Than Abstract Base Classes, Protocols Are Enforced Only Statically, FastAPI, Lifespan Owns The Container, No Authentication, Rate Limiting Or Concurrency Bound (+14 more)

### Community 50 - "Gemini Adapter"
Cohesion: 0.12
Nodes (16): Factory, T, Maps a provider name to a factory for one kind of component., Decorator registering a factory under `name`. Re-registering a name replaces…, Registry, parametrize, The registry is the mechanism that makes providers pluggable, so it is tested…, Overriding a built-in must be possible without editing it. (+8 more)

### Community 51 - "ADR 0001 Protocol Seams"
Cohesion: 0.10
Nodes (15): EmbeddingModel, Vector, Combined lexical and vector search, fused into a single ranking., A text embedding model. Document and query embedding are separate methods…, Vector width. Must match the vector store's configured dimension., Embed corpus text. Returns one vector per input, in order., Embed a search query., _build() (+7 more)

### Community 52 - "CLI Tests"
Cohesion: 0.13
Nodes (20): Session Startup Checklist, Session Startup Checklist (claude.md), Conversation and Session Memory (architecture page), session_id and history Are Mutually Exclusive, Evaluation Methodology, Manning, Raghavan & Schütze, Introduction to Information Retrieval (2008), The Metric Selection Rule (established, decisive, honest), ADR Index (0001–0014) (+12 more)

### Community 53 - "Measured Chunker Decision & IR Metrics"
Cohesion: 0.12
Nodes (20): Uniform Corpus Access Control, Cross-Encoder Reranking (off by default, unmeasured), follow_up_lift — 0.000 Off, +0.177 On, Six-Stage Retrieval Pipeline, precision@5 0.200 Is The Structural Maximum, Query Rewriting (ON by default since Phase 6), Retrieval Bounds Everything Downstream, Threshold Applied Before Reranking (+12 more)

### Community 54 - "Logging System Design"
Cohesion: 0.16
Nodes (14): LangChainDocument, Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…, Exposing OSC to LangChain, rather than the other way round. Every other…, Translate one retrieval hit into a LangChain document. The score and the match…, to_langchain_document(), _encode_vector(), Vector, PostgreSQL + pgvector store: the production default. One datastore holds chunk… (+6 more)

### Community 55 - "StoreInspector Protocol"
Cohesion: 0.13
Nodes (10): Conversation, Answer, Answerer, Message, A multi-turn question-answering session. The composition of a `SessionStore`…, The transcript so far, as the next turn would see it. For a client reconnecting…, Answer one turn in `session_id`, recording it in the session's history., Stream one turn in `session_id`, recording it when the answer completes. The… (+2 more)

### Community 56 - "VectorStore Protocol"
Cohesion: 0.14
Nodes (18): _escape(), Grounding and citation handling for providers without native citation support.…, Remove a leading `<think>` block from a reasoning model's answer. Ollama…, Fail loudly when the model produced no answer text. An empty completion…, Escape the characters that would otherwise break out of an XML-ish attribute., require_answer(), strip_reasoning(), Reasoning-model output handling in the OpenAI-compatible adapter. Hybrid… (+10 more)

### Community 58 - "Cross-Encoder Reranker"
Cohesion: 0.19
Nodes (16): FastAPI, create_app(), FastAPI application. Thin by design: it validates input, calls one pipeline…, Serve the bundled chat client at the site root. Registered outside the `/api`…, Build the ASGI application. Accepting settings makes the app constructible in…, _register_error_handlers(), _register_ui(), describe_shutdown() (+8 more)

### Community 59 - "Session Memory Tests"
Cohesion: 0.15
Nodes (18): Severity, _CaseOutcome, _judge_metric(), _outcomes(), The regression gate: does this run still clear the trusted baseline? `--fail-…, The comparable skeleton of one case or turn, from either report shape., Derive this metric's tolerance, its severity, and the sentence explaining both., How many cases actually contributed to `name`. Using the suite size for… (+10 more)

### Community 60 - "Session Store Internals"
Cohesion: 0.15
Nodes (16): Composition root. The only module that knows both which providers exist and how…, Close a component if it offers a way to be closed. Probed rather than required…, _release(), OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…, ChunkingSettings, CorpusSettings, DatabaseSettings, LoggingSettings (+8 more)

### Community 61 - "Evaluation Framework ADR"
Cohesion: 0.14
Nodes (16): NoopReranker, Truncates the candidate list without reordering it., _pipeline(), parametrize, Retrieval tests, including the vector store contract. `test_store_contract`…, This is what triggers abstention rather than a guessed answer., With no history there is nothing to resolve, so no call should be made., A degraded query beats a failed request. (+8 more)

### Community 62 - "Embeddings & Vector Width"
Cohesion: 0.12
Nodes (17): Chunk Size As The Highest-Leverage Knob, Vector Dimension Fixed In The DDL / DimensionMismatchError, Embedding Model Chosen Independently Of The Chat Model, nomic-embed-text (768 dimensions), Container Injects Vector Width And Embedding Model Id, Retrieval Configuration Knobs, Citations Are Asserted, Not Verified, 4096-Token Context Caps The Corpus Per Answer (+9 more)

### Community 63 - "Retrieval Metric Functions"
Cohesion: 0.12
Nodes (17): Every Case Records Its Trace Id, Ingestion Path, Never Let A Vendor Exception Escape An Adapter, VectorStore Protocol, ADR 0004 — Persist Traces To A Bounded JSONL File, Auto-Explain On Failure, Bounded Means Lossy — Not An Audit Log, OpenTelemetry Exporter Deferred, Span Stays OTel-Shaped (+9 more)

### Community 64 - "Reasoning-Model Hygiene"
Cohesion: 0.13
Nodes (17): capture_text Privacy Seam, The Debugging Workflow, Why a JSONL File (alternatives rejected), Observability Subsystem, render.py (waterfall renderer), store.py (append-only JSONL trace log), trace.py (context-var span tree), The ponytail: Comment Convention (+9 more)

### Community 65 - "Trace Persistence"
Cohesion: 0.23
Nodes (17): load_golden_set(), Read and validate a golden set file. Raises: EvaluationError: The file is…, Path, `make eval` runs this file; a validation error here is a broken gate. Cheap to…, The FAQ suite is kept runnable, not just kept on disk. Deleting evaluation…, Their numbers are not comparable, and the files say so themselves., test_a_missing_golden_set_names_the_file(), test_a_valid_golden_set_loads() (+9 more)

### Community 66 - "Default Local Profile"
Cohesion: 0.12
Nodes (11): A second-stage relevance model applied to retrieval candidates., Return the `top_k` most relevant candidates, most relevant first., Reranker, _build(), CrossEncoderOptions, CrossEncoderReranker, BaseModel, register (+3 more)

### Community 67 - "Observability Subsystem"
Cohesion: 0.14
Nodes (8): AssistantError, The messages this session holds, and the start of an interaction. Reading…, Read a session's state without touching its activity clock. For diagnostics…, Drop sessions untouched for longer than the TTL. Swept on access rather than on…, The session id is not known to this store. An operator problem rather than a…, One conversation's working set. `messages` alternates user and assistant and is…, SessionState, UnknownSessionError

### Community 68 - "Golden Case Validators"
Cohesion: 0.15
Nodes (9): _configuration_differences(), _detect_trade_offs(), Finding, GateReport, Any, The gate's decision and the evidence for it., Improvements that were bought with a regression elsewhere., Configuration keys that differ, so a comparison cannot silently span two… (+1 more)

### Community 69 - "Fusion & Provider Packages"
Cohesion: 0.19
Nodes (13): delete, IndexStatistics, Request, close_session(), _container(), health(), Liveness plus the active component set. Returning the resolved configuration…, What is currently indexed. Separate from `/health` because it queries the… (+5 more)

### Community 70 - "Community 70"
Cohesion: 0.22
Nodes (10): GoldenCase, ScoredChunk, CaseResult, Answer, Aggregate per-case results into the numbers a run is judged on. Two exclusions…, Everything one golden case produced, scored. Kept flat and JSON-serialisable on…, Whether this case contributed a measurement rather than an error., summarise() (+2 more)

### Community 71 - "Community 71"
Cohesion: 0.14
Nodes (13): dedupe(), hit_at_k(), ndcg_at_k(), precision_at_k(), Retrieval and generation metrics. Every function here is pure: same inputs,…, Whether any relevant document appears in the top `k`. The binary form of…, Normalised discounted cumulative gain over the top `k`. Recall asks whether the…, Collapse repeats while preserving rank order. Retrieval returns chunks and… (+5 more)

### Community 72 - "Community 72"
Cohesion: 0.17
Nodes (13): Logging Rules for New Code, Observability Rules for New Code, Logging Rules (claude.md), Observability Rules (claude.md), logging: rotation, audit, capture_payloads, log_spans, observability: persist_traces, capture_text, expose_traces, ./osc logs Is a Discovery Command, Not a Viewer, Instrument the Pipeline, Not the Adapter (+5 more)

### Community 73 - "Community 73"
Cohesion: 0.15
Nodes (12): Any, fail(), print_trace(), Plumbing shared by the CLI command modules. Kept separate so `core` and…, A table styled consistently across every command., Report an operator-facing error and exit non-zero., Render the trace the command just produced, if one was asked for., Report a failed command usefully instead of as a stack trace. Two things happen… (+4 more)

### Community 74 - "Community 74"
Cohesion: 0.19
Nodes (13): embeddings: ollama / nomic-embed-text (768-d), generation: max_tokens 1500, require_citations true, llm: ollama / qwen3:8b, config/default.yaml — Default Local Profile, reasoning_effort: none, reranker: noop (until measured), retrieval: hybrid, candidates 30, top_k 5, rrf_k 60, vector_store: pgvector (+5 more)

### Community 75 - "Community 75"
Cohesion: 0.15
Nodes (13): Add-on Tier Pricing, Cost Parameters and Profit Margins (up to 4 costs, 2 margins), Per-Variant Quantity Range Evaluation, App-Created Discount Label, Best Discount Tier Across Multiple Collections, Combined Collection Quantity Discount Slabs, OSCP Support Channel (apps@oscprofessionals.com), Offer List Drag-and-Drop Ordering (+5 more)

### Community 76 - "Community 76"
Cohesion: 0.21
Nodes (12): Cart Discount, Order Limits, Row-Level Then Order-Level Discount Ordering, Row Level Discount, FEAT-04 Cart Level Discount (SCN-006, SCN-007), FEAT-05 Order Limits Min/Max (SCN-008, SCN-009), MOQ — Minimum Order Quantity (glossary), OSCP Wholesale B2B Pricing — Scenario Document (+4 more)

### Community 77 - "Community 77"
Cohesion: 0.20
Nodes (12): Priority of the Offers, Product and Collection Page Integration, Quick Order Form, Custom Price Grid App Block / App Embed, Theme Compatibility, Tiered Pricing (collection, product and variant level), FEAT-01 Quantity Break Pricing (SCN-001, SCN-002), FEAT-07 Quick / Bulk Order Form (SCN-011) (+4 more)

### Community 78 - "Community 78"
Cohesion: 0.21
Nodes (12): Unparseable Files Are Recorded As Failures, Not Deleted, Extension-to-Parser Dict (nine extensions), Parsers Extract And Never Rewrite, Adding a Corpus Category Is Creating a Directory, Company/Engineering Corpus Split, corpus.root — The One Rule, FAQ Preserved As A Runnable Prose Control Suite, No YAML Frontmatter in Corpus Documents (+4 more)

### Community 79 - "Community 79"
Cohesion: 0.23
Nodes (5): Path, Record one completed trace. Never raises. A read-only filesystem, a full disk…, Completed traces, most recent first., A size-bounded, append-only log of completed traces. Two files: the one being…, TraceStore

### Community 80 - "Community 80"
Cohesion: 0.23
Nodes (5): BaseModel, Vector, Adapter over the Voyage AI embeddings endpoint., VoyageEmbeddingModel, VoyageOptions

### Community 81 - "Community 81"
Cohesion: 0.22
Nodes (7): BaseSettings, PydanticBaseSettingsSource, Any, field_validator, Let the environment express "no directory", which it otherwise cannot. An…, Lowest-precedence source reading a YAML profile. The profile path comes from…, _YamlProfileSource

### Community 82 - "Community 82"
Cohesion: 0.18
Nodes (11): CartDiscount — Schema, INV-9 Public Metafield Exception, oscp.cartRules (CartDiscountData offers), oscp.isCartTags (Function eligibility aggregate), DraftOrderProcessing — Schema, oscp.orderProcessingActive, oscp.orderProcessingMode, oscp.freegift_global_settings (widget copy and colors) (+3 more)

### Community 83 - "Community 83"
Cohesion: 0.18
Nodes (9): GoldenSet, compare(), EvaluationReport, Any, The on-disk shape. Stable, because baselines are compared against it., Score every case in `golden`, at most `concurrency` at a time., Metrics present in both runs, as (name, baseline, current). Only the…, One evaluation run: what was measured, under what configuration. (+1 more)

### Community 84 - "Community 84"
Cohesion: 0.18
Nodes (11): Settings, load(), log_command(), Path, Name the command that is about to run. Without it a day of history is a stream…, Resolve settings and initialise logging and tracing for one command.…, Every command initialises identically; without this they are indistinguishable., `osc ask "<a real question>"` puts user text on the command line. (+3 more)

### Community 85 - "Community 85"
Cohesion: 0.20
Nodes (10): Decision Optimisation Order, Engineering Philosophy, Failure Diagnosis Workflow, Operational Tooling (./osc CLI), OSC Engineering Handbook (AGENTS.md), Output Rules (stdout vs stderr, errors), Engineering Philosophy (claude.md), Operational Tooling (claude.md) (+2 more)

### Community 86 - "Community 86"
Cohesion: 0.20
Nodes (10): post, chat(), open_session(), The trace for `trace_id`, if it is still in the buffer. Returned inline on…, Open a conversation. Sessions are ephemeral: memory lives in this process, is…, Answer a question, streaming by default. Three shapes, one handler: a one-shot…, _trace_payload(), A session id. The only thing a client needs to keep between turns. (+2 more)

### Community 87 - "Community 87"
Cohesion: 0.20
Nodes (6): Conversational memory. Not built through a registry, unlike the five swappable…, Append one completed exchange. Raises: UnknownSessionError: No such session, or…, Destroy a session's memory. Returns whether there was one to destroy. Named…, Where conversation state lives between turns. Async because the implementation…, Open a session and return its id., SessionStore

### Community 88 - "Community 88"
Cohesion: 0.29
Nodes (4): OpenAICompatibleEmbeddingModel, Vector, Release the underlying HTTP client. `Container.shutdown()` probes every…, Adapter over the `/v1/embeddings` interface.

### Community 89 - "Community 89"
Cohesion: 0.27
Nodes (9): documents(), embeddings(), _isolate_observability(), fixture, MonkeyPatch, Path, Shared test fixtures and in-process test doubles. The doubles are deliberately…, Keep persisted traces and logs out of the working directory, and apart. Both… (+1 more)

### Community 90 - "Community 90"
Cohesion: 0.20
Nodes (10): Path, A directory of .pptx looks identical to an empty corpus in the sync report., Construction alone passes with the model unpulled or the credential expired., A failing provider must be named on one line, not raised as a traceback., test_doctor_can_skip_the_live_calls(), test_doctor_makes_live_calls_by_default(), test_doctor_passes_when_every_component_is_reachable(), test_doctor_reports_a_broken_component_and_exits_non_zero() (+2 more)

### Community 91 - "Community 91"
Cohesion: 0.20
Nodes (4): _ClosableEmbedding, Holds a resource, like the Voyage and OpenAI adapters do., Closes synchronously, to prove both shapes are handled., _SyncClosableReranker

### Community 92 - "Community 92"
Cohesion: 0.22
Nodes (9): Shopify Coupon Applied After Tier Discount, Draft Order Processing, 15-Minute Invoice Reuse Window, oscp-order-processing Order Tag, Server-Side Wholesale Price Validation, FEAT-10 Auto Order Tagging (SCN-014), Metafield (glossary), EC-07 Cart Discount Plus Shopify Native Discount Code (+1 more)

### Community 93 - "Community 93"
Cohesion: 0.25
Nodes (9): load_conversational_set(), Any, Path, Read a suite file, reporting the three ways it can fail to be one. Shared by…, Read and validate a multi-turn golden set. Raises: EvaluationError: The file is…, _read_yaml_mapping(), The suite the canonical command runs must load. A validation error here is a…, test_a_missing_conversational_set_names_the_file() (+1 more)

### Community 94 - "Community 94"
Cohesion: 0.32
Nodes (8): CSV Export and Bulk Import of Variant Rules, Email Notification Setup (three templates), B2B Registration Form, FEAT-06 B2B Registration Form (SCN-010), FEAT-09 Bulk CSV Import/Export (SCN-013), FEAT-12 Personalised Email Notifications (SCN-016), EC-14 CSV Import Conflicts With Existing Rules, FA-09 CSV Bulk Import / Export

### Community 95 - "Community 95"
Cohesion: 0.25
Nodes (8): $app:access_lock_rule metaobject, AccessLock — Schema, Metaobject field keys are immutable once created, oscp.lockTags (checkout hard-lock tags), segment.assigned (customer segment handle), extra_fee_rule metaobject, ExtraFee — Schema, oscp.extraFeeProductId (hidden fee product GID)

### Community 96 - "Community 96"
Cohesion: 0.29
Nodes (8): BulkImportExport — Schema, CSV sample templates (utils/sampleTemplates.ts), oscp.priceRule (variant quantity-break tiers), oscp.rangeRule (date-range campaign tiers), oscp.rules (product-level mirror rules), oscp.isMember (variant_level_tags), extensions/cart-transformer compatibility constraint, oscp.adt (PriceAddonData variant metafield)

### Community 97 - "Community 97"
Cohesion: 0.43
Nodes (8): Acceptance Criteria Bank (AC-01..AC-19), FA-01 Tiered / Volume Pricing, FA-03 Fixed Price Rules, FA-05 B2B Registration Form, FA-06 Quick Order Form, FA-10 Manual Order Support, Merchant Archetypes Reference (MA-01..MA-07), OSCP Wholesale B2B — Scenario Master (SCN-001..SCN-010)

### Community 98 - "Community 98"
Cohesion: 0.25
Nodes (8): MonkeyPatch, fixture, Point the CLI at in-process doubles through configuration alone. Which is the…, `AssistantError` names a problem the operator must fix; frames bury it., The trace names the stage that raised and what every earlier stage did., _stub_environment(), test_a_failure_inside_a_stage_prints_the_trace(), test_an_operator_error_is_a_message_not_a_traceback()

### Community 99 - "Community 99"
Cohesion: 0.29
Nodes (5): ChatRequestBody, MessageBody, Message, model_validator, One turn. `session_id` and `history` are two ways to supply conversational…

### Community 101 - "Community 101"
Cohesion: 0.39
Nodes (3): GeminiEmbeddingModel, Vector, Adapter over `google-genai`'s embedding interface.

### Community 102 - "Community 102"
Cohesion: 0.32
Nodes (3): LocalEmbeddingModel, Vector, Adapter over a `sentence-transformers` model loaded in-process.

### Community 103 - "Community 103"
Cohesion: 0.33
Nodes (7): Conversation Rules, fast_llm (query rewriter and judge model), retrieval.rewrite_queries: true, History Reaches Retrieval Only Through the Query Rewriter, context_switch_recovery / context_pollution, faithfulness (LLM-as-judge, opt-in), follow_up_resolution / follow_up_lift

### Community 104 - "Community 104"
Cohesion: 0.33
Nodes (7): Knowledge Corpus Rules, Knowledge Corpus Rules (claude.md), corpus.root: docs/company/schema, AddOnsTierPricing — Schema, oscp.cartTransformId, Knowledge Base Excluded from the Answer Corpus, Corpus Directory Boundary (docs/company/schema only)

### Community 105 - "Community 105"
Cohesion: 0.29
Nodes (5): ConversationalSet, ConversationalReport, Any, One multi-turn evaluation run., Score every case, at most `concurrency` sessions at a time. Concurrency is over…

### Community 106 - "Community 106"
Cohesion: 0.33
Nodes (7): Extra Fee, Free Gift, Customer Tag (glossary), FEAT-02 Customer Tag Tier Pricing (SCN-003, SCN-004), FEAT-11 Hide Shipping Methods (SCN-015), SCN-X01 Customer-Level Fixed Price per SKU (out of scope), Customer Group Matrix (All / Logged In / Wholesale / VIP)

### Community 107 - "Community 107"
Cohesion: 0.29
Nodes (7): Market-Based Offers, Tax Display, FEAT-03 Markets-Based Pricing (SCN-005), FEAT-08 Tax Display by Country (SCN-012), Shopify Market (glossary), FA-07 Multi-Currency / Markets, FA-08 Tax Display (PDP Widget)

### Community 108 - "Community 108"
Cohesion: 0.38
Nodes (7): app_settings.registractionForm (legacy spelling preserved), app_settings.approveNewCustomers, CustomerRegistration — Schema, CustomerSegment — Schema, segment.status (approved / pending), app_settings.notifications (SMTP templates), EmailConfiguration — Schema

### Community 109 - "Community 109"
Cohesion: 0.29
Nodes (7): IDEMPOTENCY_WINDOW_MS (15 min draft reuse), OrderProcessingDraft (Prisma idempotency model), An Absent Metric Is Not a Zero Metric, fact_match, Where the Architecture Is Weakest, Testing Known Gaps, Memory Does Not Survive a Restart

### Community 110 - "Community 110"
Cohesion: 0.29
Nodes (7): Exception, AssistantError, EvaluationError, Base class for every error raised by this package., An evaluation could not be run as specified. Raised for a malformed golden set,…, The vector store could not complete an operation., VectorStoreError

### Community 111 - "Community 111"
Cohesion: 0.29
Nodes (7): get, get_trace(), list_traces(), Recent execution traces, most recent first., One execution trace in full, by id or unique prefix., Recent execution traces. Development-only; see `Settings.traces_are_exposed`., TraceListBody

### Community 112 - "Community 112"
Cohesion: 0.38
Nodes (4): _cosine_similarity(), Vector, Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…, _tokenize()

### Community 113 - "Community 113"
Cohesion: 0.33
Nodes (5): ADR 0008 — Ingestion deduplicates by source, not by content, Alternatives considered, Consequences, Context, Decision

### Community 114 - "Community 114"
Cohesion: 0.33
Nodes (5): Embeddings, LangChainEmbeddingOptions, BaseModel, _FakeEmbeddings, A LangChain `Embeddings` with no dependencies. LangChain's own…

### Community 115 - "Community 115"
Cohesion: 0.40
Nodes (6): corpus(), Document, fixture, StubEmbeddingModel, A three-document corpus with `relative_path` set, as the loader would., retrieval()

### Community 116 - "Community 116"
Cohesion: 0.40
Nodes (4): Answerer, FaithfulnessJudge, RetrievalPipeline, Settings

### Community 117 - "Community 117"
Cohesion: 0.40
Nodes (5): Measured Chunker Comparison Table, chunking: markdown 900/120, Järvelin & Kekäläinen, ACM TOIS 20(4), 2002, mrr (mean reciprocal rank), ndcg@k

### Community 118 - "Community 118"
Cohesion: 0.40
Nodes (5): 3072-Dimension Embedding Caveat, 384-Dimension Database Separation, BGE Asymmetric Query Prefix, cross_encoder Reranker (ms-marco-MiniLM-L-6-v2), local-only Experiment Profile

### Community 119 - "Community 119"
Cohesion: 0.40
Nodes (5): ContextVar, T, Restore `variable`, tolerating a close in a foreign context. The streaming…, _reset(), Token

### Community 120 - "Community 120"
Cohesion: 0.40
Nodes (4): Conversation, FaithfulnessJudge, RetrievalPipeline, Settings

### Community 121 - "Community 121"
Cohesion: 0.40
Nodes (5): Container — Composition Root and Lifecycle, The Five Seams (protocols.py), Protocols, Not Base Classes, Registries (name to factory), Vendor Agnosticism — Business Logic Never Imports A Provider

### Community 122 - "Community 122"
Cohesion: 0.40
Nodes (4): encode_event(), Any, Server-sent event encoding. SSE rather than WebSockets: the stream is one-…, Encode one named SSE frame. The payload is serialised without literal newlines…

### Community 124 - "Community 124"
Cohesion: 0.50
Nodes (4): parametrize, Regression: `input_tokens` contains "token" and is a cost measurement. The…, test_credential_fields_are_redacted(), test_token_counts_are_not_mistaken_for_credentials()

### Community 125 - "Community 125"
Cohesion: 0.33
Nodes (4): The property that makes disk bounded rather than merely monitored., An operational problem, not a reason to refuse to start. Console logging still…, test_an_unwritable_log_directory_does_not_stop_the_process(), test_retention_deletes_the_oldest_rather_than_keeping_it()

### Community 126 - "Community 126"
Cohesion: 0.67
Nodes (3): AutoOrderTag — Schema, oscpB2B.autoTagStatus, oscpB2B.warehouse / oscpB2B.brand product metafield definitions

### Community 128 - "Community 128"
Cohesion: 0.67
Nodes (3): LangChain Scope Rule (adopt undifferentiated work only), OSCRetriever (outbound LangChain BaseRetriever), Tracing Is OSC's Own, Not OpenTelemetry

### Community 129 - "Community 129"
Cohesion: 0.67
Nodes (3): fixture, Leave the root logger as it was found. The handler stack and the listener…, _restore_logging()

## Ambiguous Edges - Review These
- `oscp.priceRule (variant quantity-break tiers)` → `oscp.isMember (variant_level_tags)`  [AMBIGUOUS]
  docs/company/schema/schema-4.md · relation: shares_data_with
- `markdown Adopted As Default Chunker on Evidence (ADR 0012)` → `LangChain`  [AMBIGUOUS]
  docs/engineering/technologies/langchain.md · relation: conceptually_related_to

## Knowledge Gaps
- **106 isolated node(s):** `osc-assistant`, `Logging and tracing are not the same thing`, `Where logs go`, `Four properties that are load-bearing`, `Coverage comes from the span bridge` (+101 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `oscp.priceRule (variant quantity-break tiers)` and `oscp.isMember (variant_level_tags)`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `markdown Adopted As Default Chunker on Evidence (ADR 0012)` and `LangChain`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `evaluate_gate()` connect `Provider Registration & Embeddings` to `Regression Gate Engine`, `Session Memory Tests`, `Golden Case Validators`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `Document` connect `Conversational Evaluator` to `FastAPI Routes & Session Endpoints`, `Protocol Seams & Container`, `Ingestion Loaders & Parsers`, `Error Hierarchy`, `PgVector Store`, `AccessLock & BulkImportExport Schemas`, `LangChain Integration Tests`, `Golden Set & Case Results`, `Eval CLI Command`, `Memory Vector Store`, `Evaluation Framework Rationale`, `Recursive Chunker`, `Quality Report Renderer`, `ADR 0001 Protocol Seams`, `Logging System Design`, `Default Local Profile`, `Community 89`, `Community 91`, `Community 114`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Container` connect `RRF Fusion & Citation Parsing` to `Test Doubles & Stubs`, `PgVector Store`, `Core CLI Commands`, `PgVector SQL & Inspection`, `Span Tree & Trace Core`, `Regression Gate Engine`, `LangChain Integration Tests`, `Community 87`, `StoreInspector Protocol`, `Cross-Encoder Reranker`, `Community 91`, `Session Store Internals`, `Evaluation Framework Rationale`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Container` (e.g. with `Conversation` and `InMemorySessionStore`) actually correct?**
  _`Container` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `MemoryVectorStore` (e.g. with `FailingChatModel` and `NativeCitationChatModel`) actually correct?**
  _`MemoryVectorStore` has 4 INFERRED edges - model-reasoned connections that need verification._