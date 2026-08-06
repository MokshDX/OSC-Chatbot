# Graph Report - /Users/mokshdutt/Developer/OFC/chatbot  (2026-08-06)

## Corpus Check
- 1 files · ~159,508 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2184 nodes · 4877 edges · 130 communities (104 shown, 26 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 491 edges (avg confidence: 0.72)
- Token cost: 30,000 input · 0 output

## Community Hubs (Navigation)
- LangChain Bridges & Splitters
- Logging Tests & CLI Command Record
- Answer Generation & Faithfulness Judge
- pgvector Store & Integration Tests
- Testing Architecture (Four Tiers)
- Error Hierarchy & Embedding Providers
- Citation Parsing & Gemini Chat
- Ingestion Pipeline & Loaders
- Composition Root & Settings Models
- Golden Set Schema & Validation
- HTTP Layer Tests
- Settings Sources & Tests
- RRF Fusion & Source Rendering
- Container Lifecycle & E2E
- Evaluation CLI Command
- In-Memory Vector Store
- Chunker Registration & Options
- Protocol Seams & Embedding Errors
- Module Map & Dependency Rules
- Diagnostic CLI Commands
- Logging Subsystem Core
- Trace Configuration & CLI Trace
- Store Construction & Embedding Calls
- Grounded Prompt & LangChain Chat
- Anthropic Adapter & Retrieval Pipeline
- Shared Test Fixtures & Retrieval Tests
- CLI Core Commands
- Corpus Boundary & Golden Set Curation
- Parser Registry & Parser Tests
- Evaluator & Judge Composition
- Stub Chat Model & Answerer Tests
- Recursive & Markdown Splitting
- Golden Set Loading & Evaluation Tests
- Server Lifecycle Tests
- Trace Store Tests
- Component Registry
- Reranker Protocol & Provider Registration
- Engineering Handbook Rules
- Span Tree & Trace Core
- Provider Errors & ChatModel Protocol
- VectorStore Errors & Inspection
- Chunking & Embedding Architecture
- API Request & Response Schemas
- Search Strategies & Reranking
- Evaluation Harness & CI Gate
- Audit Stream, Redaction & osc logs
- Architecture Overview & Weak Points
- Citation Grounding & Reasoning Models
- Chunk Types & Document Chunks
- CLI Command Tests
- Evaluation Metrics
- Fusion & Store Statistics
- Retrieval Architecture & Metrics
- FastAPI Application Assembly
- Doctor Health Checks
- OpenAI-Compatible Chat Provider
- Parse Errors & Format Parsers
- Chunk Size & Vector Dimension Decisions
- Filesystem Loader & Title Derivation
- Persistent Trace Store
- Ingestion Logging & Trace Persistence
- Chat & Health Endpoints
- Logging Documentation & ADR 0009
- Graphify Graph Findings
- Whitespace Normalisation & Error Base
- Add-on Tier Pricing & Discount Slabs
- Chunker Factories & Pipeline Wiring
- Observability Entry & Trace Rendering
- Experiment Profiles & Embedding Caveats
- Cart Discount & Order Limits
- Offer Priority & Storefront Integration
- Ponytail Discipline & Evaluation Framework
- Trace Sink & JSONL Parsing
- Voyage Embeddings
- The Logging System & Span Bridge
- Local Embedding Model
- Session Startup & Deduplication (ADR 0008)
- ADR 0009 Structure
- Trace & Status Endpoints
- HTML Parser
- OpenAI-Compatible Embeddings
- Doctor Command Tests
- Draft Order Processing
- Chat Web UI
- Trace Listing CLI
- Observability Installation & Isolation
- B2B Registration, Export & Notifications
- Scenario Acceptance Criteria Bank
- CLI Test Environment Doubles
- Startup Banner & Lifecycle
- Trace Ring Buffer
- Gemini Embeddings
- Noop Reranker & Evaluation Corpus
- Citations & Native Citation Model
- Default Configuration Profile
- Observability Config & Rationale
- Extra Fee, Free Gift & Customer Tags
- Markets Pricing & Tax Display
- Trace Persistence Decision (ADR 0004)
- ADR 0008 Content Deduplication
- Evaluation Run Comparison
- Abstention Policy & Output Streams
- Golden Set Curation Rules
- Inspection Payloads & Redaction
- Judge Verdict Parsing
- Generation Package & Prompts
- Database Schema
- Content Hashing
- Groq + Voyage Profile
- Development Database Compose
- osc Launcher Script
- Outbound Integrations Package
- Credential Redaction in CLI Config
- Explain Flag Debugging Loop
- Traces Across Process Boundaries
- Most Recent Trace Expansion
- Trace Filtering by Name
- Unreachable Service Reporting
- Help Command Grouping
- Hosted Model Prompt Budget
- Hosted Anthropic Profile
- Bridge Profile Local Embeddings
- Heading-Aware Markdown Chunking
- LangChain Bridge Profile
- Package Metadata
- Any Type Alias
- Generic Type Var
- TestClient Symbol
- MonkeyPatch Symbol

## God Nodes (most connected - your core abstractions)
1. `MemoryVectorStore` - 72 edges
2. `Document` - 66 edges
3. `StubEmbeddingModel` - 65 edges
4. `ComponentConfig` - 64 edges
5. `Container` - 60 edges
6. `ChatRequest` - 59 edges
7. `PgVectorStore` - 43 edges
8. `ScoredChunk` - 40 edges
9. `StubChatModel` - 40 edges
10. `Settings` - 36 edges

## Surprising Connections (you probably didn't know these)
- `FEAT-01 Quantity Break Pricing (SCN-001, SCN-002)` --semantically_similar_to--> `Add-on Tier Pricing`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_B2B_Scenario_Document-1_cb06f24b.md → docs/company/faq/add-on-tier-pricing.md
- `FEAT-04 Cart Level Discount (SCN-006, SCN-007)` --semantically_similar_to--> `Cart Discount`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_B2B_Scenario_Document-1_cb06f24b.md → docs/company/faq/cart-discount.md
- `FA-10 Manual Order Support` --semantically_similar_to--> `Draft Order Processing`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_Wholesale_B2B_Scenario_Templates_0ba70067.md → docs/company/faq/draft-order.md
- `Operational Tooling (./osc CLI)` --semantically_similar_to--> `Operational Tooling (claude.md)`  [INFERRED] [semantically similar]
  AGENTS.md → claude.md
- `Quantity Clubbed for Variants of a Product` --semantically_similar_to--> `Per-Variant Quantity Range Evaluation`  [INFERRED] [semantically similar]
  graphify-out/converted/Use Cases _ OSCP Wholesale B2B App - Quantity Clubbed for Product Asset 2025_51fc9cac.md → docs/company/faq/add-on-tier-pricing.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **What Makes the Fast Tier Meaningful** — docs_engineering_architecture_testing_unit_component_tier, docs_engineering_architecture_testing_protocol_layer_doubles, docs_engineering_architecture_testing_conftest, docs_engineering_architecture_testing_stubembeddingmodel, docs_engineering_architecture_testing_stubchatmodel, docs_engineering_architecture_testing_registry_registration_of_doubles, docs_engineering_architecture_provider_architecture [EXTRACTED 1.00]
- **Four-Tier Confidence Ladder** — docs_engineering_architecture_testing_unit_component_tier, docs_engineering_architecture_testing_integration_tier, docs_engineering_architecture_testing_e2e_tier, docs_engineering_architecture_testing_evaluation_tier, docs_engineering_architecture_testing_correctness_versus_goodness [EXTRACTED 1.00]
- **Test Isolation Discipline (Corpus, Working Directory, Environment)** — docs_engineering_architecture_testing_never_touch_production_corpus, docs_engineering_architecture_testing_never_write_working_directory, docs_engineering_architecture_testing_e2e_corpus_violation_repair, docs_engineering_architecture_testing_env_purge_isolation_defect, docs_engineering_architecture_testing_conftest [EXTRACTED 1.00]
- **The Four Load-Bearing Properties of the Logging System** — docs_engineering_architecture_logging_async_queue_writes, docs_engineering_architecture_logging_trace_id_correlation, docs_engineering_architecture_logging_bounded_disk_rotation, docs_engineering_architecture_logging_redaction_filter, docs_engineering_architecture_logging_logging_system [EXTRACTED 1.00]
- **Measurement-Before-Change Discipline** — project_status_evaluation_framework, project_status_measured_improvement_rule, project_status_deterministic_gate_judge_optin, project_status_document_level_relevance, project_status_milestone_spend_the_harness, readme_test_vs_eval [INFERRED 0.85]
- **The Guarantees Behind a Grounded Answer** — project_status_architectural_abstention, project_status_citation_strength_gap, project_status_frozen_prompts, project_status_parsers_plain_dict, project_status_hybrid_retrieval_rrf [INFERRED 0.85]
- **The Failure Diagnosis Loop** — agents_operational_tooling, agents_diagnosing_a_failure, docs_engineering_architecture_observability_debugging_workflow, docs_engineering_architecture_logging_audit_stream [EXTRACTED 1.00]
- **The docs/company vs docs/engineering Boundary** — agents_knowledge_corpus_rules, docs_engineering_readme_knowledge_base [INFERRED 0.85]
- **Streamed grounded answer flow in the web client** — src_osc_assistant_api_static_index_submithandler, src_osc_assistant_api_static_index_rendersources, src_osc_assistant_api_static_index_ssestreamprotocol, src_osc_assistant_api_static_index_completeeventauthority, src_osc_assistant_api_static_index_groundedanswercontract [EXTRACTED 1.00]
- **Tier price precedence resolution across variant, product and collection scopes** — docs_company_faq_priority_of_the_offers_offer_priority, docs_company_faq_priority_of_the_offers_offer_list_ordering, docs_company_faq_tiered_pricing_guide_tiered_pricing, docs_company_faq_combined_collection_quantity_discount_slabs_best_tier_across_collections, graphify_out_converted_oscp_wholesale_b2b_scenario_templates_0ba70067_ec_01_multiple_tag_discount_conflict [INFERRED 0.85]
- **B2B account onboarding: registration, notification, approval, tag-gated pricing** — docs_company_faq_registration_form_registration_form, docs_company_faq_registration_form_email_notification_setup, graphify_out_converted_oscp_b2b_scenario_document_1_cb06f24b_feat_06_b2b_registration_form, graphify_out_converted_oscp_b2b_scenario_document_1_cb06f24b_feat_12_email_notifications, graphify_out_converted_oscp_wholesale_b2b_scenario_templates_0ba70067_fa_05_b2b_registration_form [INFERRED 0.85]
- **Delivering the wholesale price at checkout via Draft Orders** — docs_company_faq_draft_order_draft_order_processing, docs_company_faq_draft_order_server_side_price_validation, docs_company_faq_draft_order_invoice_reuse_window, docs_company_faq_draft_order_oscp_order_processing_tag, docs_company_faq_draft_order_coupon_after_tier_discount_ordering [EXTRACTED 1.00]
- **The Five Swappability Protocols** — docs_engineering_architecture_provider_architecture_chatmodel_protocol, docs_engineering_architecture_provider_architecture_embeddingmodel_protocol, docs_engineering_architecture_provider_architecture_vectorstore_protocol, docs_engineering_architecture_provider_architecture_reranker_protocol, docs_engineering_architecture_provider_architecture_chunker_protocol [EXTRACTED 1.00]
- **Enforcing The Corpus Boundary** — docs_engineering_architecture_knowledge_corpus_corpus_boundary_rule, docs_engineering_decisions_0007_knowledge_corpus_layout_exclusion_list_rejected, docs_engineering_architecture_knowledge_corpus_access_control_uniformity [INFERRED 0.95]
- **Scoped LangChain adoption: bridge providers, heading-aware splitting, the experiment profile and the citation cost it carries** — config_experiments_langchain_bridge_profile, config_experiments_langchain_bridge_markdown_chunking [INFERRED 0.85]

## Communities (130 total, 26 thin omitted)

### Community 0 - "LangChain Bridges & Splitters"
Cohesion: 0.05
Nodes (54): LangChainDocument, _heading_path(), LangChainChunkerOptions, Any, Join whichever heading levels are present into a readable path., `ChunkerOptions` plus the settings only the LangChain splitters expose., _require_splitters(), _section_metadata() (+46 more)

### Community 1 - "Logging Tests & CLI Command Record"
Cohesion: 0.07
Nodes (60): log_command(), Name the command that is about to run. Without it a day of history is a stream…, fixture, parametrize, Path, Persistent logging tests. Logging is the system that gets read when something…, The property that makes disk bounded rather than merely monitored., An interactive command prints its answer; the file still records everything.… (+52 more)

### Community 2 - "Answer Generation & Faithfulness Judge"
Cohesion: 0.07
Nodes (43): AnswerEvent, LLM-as-judge faithfulness scoring. Faithfulness asks whether every claim in an…, _annotate_abstention(), _annotate_generation(), AnswerComplete, _audit_answer(), Answer generation: the composition of retrieval and a chat model. This is the…, Answer `question`, emitting events as they become available. (+35 more)

### Community 3 - "pgvector Store & Integration Tests"
Cohesion: 0.07
Nodes (40): PgVectorOptions, PgVectorStore, BaseModel, Adapter over PostgreSQL with the pgvector extension., The partition this store reads and writes. Every query is scoped to it., Replace a document and its chunks in a single transaction. Delete-then-insert…, EmbeddedChunk, A chunk paired with the vector produced for it, tagged with its model. The… (+32 more)

### Community 4 - "Testing Architecture (Four Tiers)"
Cohesion: 0.06
Nodes (46): evaluation.md (The Fourth Tier), provider-architecture.md (Protocols Not ABCs), Testing Architecture (Four Tiers), Rule: A Test Asserts a Behaviour, Not an Implementation, conftest.py (Shared Fixtures and Isolation), Correctness vs Goodness Distinction, The test_e2e.py Corpus-Root Violation and Repair, End-to-End Tier (make test-e2e) (+38 more)

### Community 5 - "Error Hierarchy & Embedding Providers"
Cohesion: 0.07
Nodes (28): Embeddings, ConfigurationError, DimensionMismatchError, MissingDependencyError, The system is misconfigured and cannot start or serve a request. Raised for…, A provider was selected but its optional dependency is not installed., The configured embedding model does not match the store's vector width.…, GeminiEmbeddingOptions (+20 more)

### Community 6 - "Citation Parsing & Gemini Chat"
Cohesion: 0.10
Nodes (26): parse_marker_citations(), Extract citations from `[n]` markers in `text`. Markers referring to a source…, _build_contents(), _finish_reason(), GeminiChatModel, _parse_usage(), Any, StreamEvent (+18 more)

### Community 7 - "Ingestion Pipeline & Loaders"
Cohesion: 0.10
Nodes (36): InMemoryLoader, Serves a fixed list of documents. Used by tests and the evaluation harness., IngestionPipeline, Chunk, embed and store one document. Each of the three stages gets its own…, Delete indexed documents that the source no longer offers. `keep` is every…, Chunks, embeds and stores documents., Sync `documents` into the store. Args: documents: The full current contents of…, Document (+28 more)

### Community 8 - "Composition Root & Settings Models"
Cohesion: 0.08
Nodes (32): Composition root. The only module that knows both which providers exist and how…, ChunkingSettings, DatabaseSettings, GenerationSettings, LoggingSettings, ObservabilitySettings, BaseModel, Configuration. Layered, highest precedence first: process environment, then… (+24 more)

### Community 9 - "Golden Set Schema & Validation"
Cohesion: 0.09
Nodes (27): field_validator, model_validator, document_key(), GoldenCase, GoldenSet, BaseModel, The golden set: the questions an evaluation run is scored against. A golden set…, A named, versioned collection of cases. (+19 more)

### Community 10 - "HTTP Layer Tests"
Cohesion: 0.09
Nodes (37): Document, TestClient, client(), _development_client(), _parse_sse(), fixture, parametrize, HTTP layer tests. These run the real application — real container, real… (+29 more)

### Community 11 - "Settings Sources & Tests"
Cohesion: 0.10
Nodes (30): BaseSettings, PydanticBaseSettingsSource, load_settings(), Any, Lowest-precedence source reading a YAML profile. The profile path comes from…, Build settings, applying `overrides` at the highest precedence., _YamlProfileSource, _isolate_environment() (+22 more)

### Community 12 - "RRF Fusion & Source Rendering"
Cohesion: 0.10
Nodes (33): Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…, reciprocal_rank_fusion(), _escape(), Escape the characters that would otherwise break out of an XML-ish attribute., Render sources as a delimited block for inclusion in a prompt. The delimiter…, render_sources(), _chunk(), _ranking() (+25 more)

### Community 13 - "Container Lifecycle & E2E"
Cohesion: 0.06
Nodes (22): Self, Container, A cheaper model for auxiliary steps such as query rewriting., Release everything that was actually built. Only components whose…, Close a component if it offers a way to be closed. Probed rather than required…, Builds and owns the application's components., _release(), OSC internal knowledge assistant. A provider-agnostic retrieval-augmented… (+14 more)

### Community 14 - "Evaluation CLI Command"
Cohesion: 0.12
Nodes (30): _assert_golden_set_is_resolvable(), _default_output(), _enforce_thresholds(), eval(), _execute(), _print_comparison(), _print_report(), command (+22 more)

### Community 15 - "In-Memory Vector Store"
Cohesion: 0.08
Nodes (21): MemoryVectorStore, A dictionary-backed `VectorStore`., Replace a document and its chunks. Atomic by construction: the vectors are…, indexed(), fixture, Store inspection tests. `StoreInspector` is what the operational commands are…, The last step of verifying a citation: the exact text the model was shown., The protocol is optional; a store that cannot support it is still a store. Both… (+13 more)

### Community 16 - "Chunker Registration & Options"
Cohesion: 0.15
Nodes (26): Chunking strategies. Imported for registration side effects., ChunkerOptions, BaseModel, Splits on the coarsest separator that keeps chunks under the target size. Falls…, RecursiveChunker, _document(), Chunking tests. Chunk id stability is the load-bearing property here: ingestion…, Chunk text is quoted back to users as citation evidence, so the chunker must… (+18 more)

### Community 17 - "Protocol Seams & Embedding Errors"
Cohesion: 0.11
Nodes (20): Exception hierarchy for the assistant. A single root (`AssistantError`) lets…, EmbeddingModel, The five seams of the system. Every swappable component is defined here as a…, A text embedding model. Document and query embedding are separate methods…, Vector width. Must match the vector store's configured dimension., _build(), register, Google Gemini embedding provider. (+12 more)

### Community 18 - "Module Map & Dependency Rules"
Cohesion: 0.09
Nodes (30): Business Logic Imports protocols And types Only, integrations/ May Import The Core; The Core May Never Import integrations/, Module Map, ChatModel Protocol, EmbeddingModel Protocol, Layered Configuration (env > .env > YAML profile), PEP 544 — Structural Subtyping, Reranker Protocol (+22 more)

### Community 19 - "Diagnostic CLI Commands"
Cohesion: 0.14
Nodes (30): Settings, chunk(), config(), doctor(), document(), documents(), logs(), providers() (+22 more)

### Community 20 - "Logging Subsystem Core"
Cohesion: 0.10
Nodes (21): LogRecord, _AuditOnly, configure_logging(), _ExcludeAudit, JsonFormatter, log_directory(), _NonDestructiveQueueHandler, Path (+13 more)

### Community 21 - "Trace Configuration & CLI Trace"
Cohesion: 0.11
Nodes (28): Expand one execution trace into a stage-by-stage waterfall. With no id this…, trace(), configure_tracing(), Install tracing configuration. Safe to call more than once., fixture, Tracing tests. The load-bearing properties are that a trace describes the…, A corpus-wide ingestion must not grow one trace without bound., Trace ids are pasted by hand out of a log line or a support ticket. (+20 more)

### Community 22 - "Store Construction & Embedding Calls"
Cohesion: 0.07
Nodes (16): Build the store, injecting values it cannot know on its own. Vector width, the…, Vector, Remove a document and every chunk belonging to it., Map document id to stored content hash, for incremental sync., Every document id currently indexed., Lexical search. Return `[]` if the store has no lexical index., Combined lexical and vector search, fused into a single ranking., Embed corpus text. Returns one vector per input, in order. (+8 more)

### Community 23 - "Grounded Prompt & LangChain Chat"
Cohesion: 0.12
Nodes (22): compose_grounded_system(), Fold the system prompt, citation instruction and sources into one string. Used…, _build(), _instantiate(), LangChainChatModel, _parse_usage(), Any, register (+14 more)

### Community 24 - "Anthropic Adapter & Retrieval Pipeline"
Cohesion: 0.11
Nodes (20): AnthropicChatModel, AnthropicOptions, _build(), _build_messages(), _last_user_index(), _parse_content(), _parse_usage(), Any (+12 more)

### Community 25 - "Shared Test Fixtures & Retrieval Tests"
Cohesion: 0.13
Nodes (21): documents(), embeddings(), fixture, Vector, Shared test fixtures and in-process test doubles. The doubles are deliberately…, A deterministic bag-of-words embedder. Hashes each token into a fixed number of…, store(), StubEmbeddingModel (+13 more)

### Community 26 - "CLI Core Commands"
Cohesion: 0.12
Nodes (26): Any, ExplainOption, _answer_payload(), ask(), ingest(), _print_answer(), Argument, command (+18 more)

### Community 27 - "Corpus Boundary & Golden Set Curation"
Cohesion: 0.08
Nodes (28): Parsers Extract And Never Rewrite, An Absent Metric Is Not A Zero Metric, Abstention Cases In The Golden Set, Relevance Scored At Document Level, Golden Set (86 cases), Golden-Set Path Guard Against The Index, Uniform Access Control, Directory As The Boundary, Corpus Boundary Enforced At Index Time (+20 more)

### Community 28 - "Parser Registry & Parser Tests"
Cohesion: 0.13
Nodes (26): parse(), Extract `path` using the parser registered for its extension. Raises:…, Path, Text extraction and multi-format loading tests. Two properties are load-bearing…, A spreadsheet's meaning is two-dimensional; retrieval is not. The row is the…, A page-image PDF parses cleanly and yields nothing. Indexing an empty document…, The pipeline is handed this list before iteration and reads it after, so a re-…, Provenance is denormalised onto every chunk, so it has to be right here. (+18 more)

### Community 29 - "Evaluator & Judge Composition"
Cohesion: 0.18
Nodes (21): FaithfulnessJudge, Scores one answer against the passages it was generated from., Evaluator, Runs a golden set and scores it. Takes the pipelines rather than the…, Answerer, Answers a question against the indexed corpus., Composes rewriting, search and reranking into one call., RetrievalPipeline (+13 more)

### Community 30 - "Stub Chat Model & Answerer Tests"
Cohesion: 0.14
Nodes (22): A chat model that returns a scripted reply. `supports_citations` is False, so…, StubChatModel, _answerer(), Answer generation tests. The abstention policy is the system's main defence…, Both citation paths must produce the same shape for downstream code., The complete event is authoritative: clients discard streamed text when it…, Generating from nothing is guessing, so the model is never invoked., test_citation_requirement_can_be_relaxed() (+14 more)

### Community 31 - "Recursive & Markdown Splitting"
Cohesion: 0.10
Nodes (19): LangChainRecursiveChunker, MarkdownChunker, Heading-aware splitting: structure first, then size. Two passes, because either…, `RecursiveCharacterTextSplitter` behind the OSC `Chunker` protocol., _build_fixed(), _build_recursive(), _chunk_id(), FixedSizeChunker (+11 more)

### Community 32 - "Golden Set Loading & Evaluation Tests"
Cohesion: 0.14
Nodes (16): load_golden_set(), Path, Read and validate a golden set file. Raises: EvaluationError: The file is…, parametrize, Path, Evaluation harness tests. The harness is the instrument every future retrieval…, test_a_missing_golden_set_names_the_file(), test_a_valid_golden_set_loads() (+8 more)

### Community 33 - "Server Lifecycle Tests"
Cohesion: 0.12
Nodes (24): exploding_client(), TestClient, Startup, shutdown and in-flight failure behaviour of the service. These cover…, A condition worth interrupting a developer for belongs in the log as well., A client told nothing waits forever. The handler previously caught only…, An unexpected exception's message is not part of the API contract., `AssistantError` messages are written for operators and are safe to surface., Only the vector store was closed before; provider HTTP clients leaked. (+16 more)

### Community 34 - "Trace Store Tests"
Cohesion: 0.18
Nodes (24): _isolated_tracing(), fixture, Path, Persisted trace tests. The store exists so a one-shot CLI command's trace…, Discarding everything at the moment the limit is hit is reliably the moment…, A truncated final line is expected: the writer may have been killed., Instrumentation must never be the reason a request fails., Nothing should be written by a process that is not tracing. (+16 more)

### Community 35 - "Component Registry"
Cohesion: 0.11
Nodes (18): Factory, A component was requested by a name that is not registered., UnknownComponentError, T, Maps a provider name to a factory for one kind of component., Decorator registering a factory under `name`. Re-registering a name replaces…, Registry, parametrize (+10 more)

### Community 36 - "Reranker Protocol & Provider Registration"
Cohesion: 0.10
Nodes (14): A second-stage relevance model applied to retrieval candidates., Reranker, Provider implementations. Importing this package registers every built-in…, _build(), CrossEncoderOptions, CrossEncoderReranker, BaseModel, register (+6 more)

### Community 37 - "Engineering Handbook Rules"
Cohesion: 0.13
Nodes (22): Failure Diagnosis Ladder, Engineering Philosophy, Knowledge Corpus Rules, Logging Rules for New Code, Measurement Rules, Observability Rules for New Code, Operational Tooling (./osc CLI), Optimisation Priority Order (+14 more)

### Community 38 - "Span Tree & Trace Core"
Cohesion: 0.13
Nodes (16): ContextVar, _log_trace(), Any, T, One stage of processing, timed. `offset_ms` is measured from the start of the…, Attach structured facts about what this stage did. Values should be small and…, Everything one operation did, as a flat list of spans in start order. Flat…, The leaf span that consumed the most wall time. Leaves only: a parent's… (+8 more)

### Community 39 - "Provider Errors & ChatModel Protocol"
Cohesion: 0.10
Nodes (14): ProviderError, An upstream provider (LLM, embeddings, reranker) failed., ChatModel, StreamEvent, A text-generating model., The provider's identifier for the underlying model, for logs and traces., True if the provider resolves citations itself from structured sources. When…, Generate a complete response. (+6 more)

### Community 40 - "VectorStore Errors & Inspection"
Cohesion: 0.12
Nodes (13): The vector store could not complete an operation., VectorStoreError, Indexed documents, newest first. `search` matches title or source URI., One document's index record, or None if it is not indexed., PostgreSQL + pgvector store: the production default. One datastore holds chunk…, Open the pool and, unless disabled, apply pending migrations., Decode JSONB into Python objects instead of raw strings., Strip the password from a DSN before it reaches a terminal or a log. Connection… (+5 more)

### Community 41 - "Chunking & Embedding Architecture"
Cohesion: 0.14
Nodes (21): Chunk Denormalises Title And Source URI, Shared Chunk Id Helper And Idempotent Ingestion, Chunking And Embedding Pipeline, EmbeddedChunk Carries Its Embedding Model Id, fixed Chunking Strategy, langchain_recursive Chunking Strategy, markdown Chunking Strategy, Unparseable Files Are Recorded As Failures, Not Deleted (+13 more)

### Community 42 - "API Request & Response Schemas"
Cohesion: 0.15
Nodes (15): AnswerBody, ChatRequestBody, CitationBody, MessageBody, Any, BaseModel, HTTP request and response models. These are separate from the domain types in…, The final answer. `abstained` is authoritative: when true the assistant… (+7 more)

### Community 43 - "Search Strategies & Reranking"
Cohesion: 0.15
Nodes (12): Return the `top_k` most relevant candidates, most relevant first., _cosine_similarity(), Vector, Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…, _tokenize(), _encode_vector(), Vector, Render a vector in pgvector's literal form for the `::vector` cast. (+4 more)

### Community 44 - "Evaluation Harness & CI Gate"
Cohesion: 0.13
Nodes (20): abstention_accuracy, CI Gate via --fail-under, citation_coverage / citation_precision, Committed Baselines, Configuration Travels With The Numbers, Evaluation Harness, groundedness, hit_rate@k (+12 more)

### Community 45 - "Audit Stream, Redaction & osc logs"
Cohesion: 0.11
Nodes (20): The Audit Stream, Disk Bounded by Construction, Corpus Text Reduced to a Length, ./osc logs Is a Discovery Command, Not a Viewer, Redaction Filter and NEVER_REDACT, QueueHandler.prepare() Strips exc_info, The Failure Modes of a Logging System Are Silent, Size-Based Rotation, Not Time-Based (+12 more)

### Community 46 - "Architecture Overview & Weak Points"
Cohesion: 0.11
Nodes (20): Where The Architecture Is Weakest, Frozen Dataclasses For Domain Types, Operator Errors Are Messages; Bugs Are Tracebacks, Never Let A Vendor Exception Escape An Adapter, Query Rewriting (off by default), FastAPI, No Authentication, Rate Limiting Or Concurrency Bound, There Is No Write Endpoint (+12 more)

### Community 47 - "Citation Grounding & Reasoning Models"
Cohesion: 0.15
Nodes (18): Grounding and citation handling for providers without native citation support.…, Remove a leading `<think>` block from a reasoning model's answer. Ollama…, Fail loudly when the model produced no answer text. An empty completion…, require_answer(), strip_reasoning(), Reasoning-model output handling in the OpenAI-compatible adapter. Hybrid…, A block that never closes means the budget ran out mid-thought., The pattern is anchored to the start deliberately: a source document about… (+10 more)

### Community 48 - "Chunk Types & Document Chunks"
Cohesion: 0.13
Nodes (11): Every chunk of a document, in ordinal order., One chunk with its full text — what the model was actually shown., Split `document`. Chunk ids must be stable across runs for the same input., Any, Apply unapplied migration files in filename order. A hand-rolled runner rather…, Fail loudly if the stored vector width disagrees with the active model.…, _to_chunk(), Chunk (+3 more)

### Community 50 - "Evaluation Metrics"
Cohesion: 0.11
Nodes (18): dedupe(), hit_at_k(), mean(), percentile(), precision_at_k(), Retrieval and generation metrics. Every function here is pure: same inputs,…, Nearest-rank percentile of `values`. Nearest-rank rather than interpolated:…, Collapse repeats while preserving rank order. Retrieval returns chunks and… (+10 more)

### Community 51 - "Fusion & Store Statistics"
Cohesion: 0.12
Nodes (13): Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…, Corpus-wide counts and chunk-size distribution., Vector store providers. Imported for registration side effects., _build(), _percentile(), register, In-process vector store. Not a toy: this is what makes the test suite run…, Nearest-rank percentile over a pre-sorted list. Empty input is 0. (+5 more)

### Community 52 - "Retrieval Architecture & Metrics"
Cohesion: 0.16
Nodes (18): recall@k, VectorStore Protocol, Cormack, Clarke & Buettcher, Reciprocal Rank Fusion (SIGIR 2009), Hybrid Search (default), Keyword Search (tsvector / BM25-equivalent), Six-Stage Retrieval Pipeline, Reciprocal Rank Fusion (k = 60), min_score Applied Before Reranking (+10 more)

### Community 53 - "FastAPI Application Assembly"
Cohesion: 0.18
Nodes (15): FastAPI, create_app(), FastAPI application. Thin by design: it validates input, calls one pipeline…, Serve the bundled chat client at the site root. Registered outside the `/api`…, Build the ASGI application. Accepting settings makes the app constructible in…, _register_error_handlers(), _register_ui(), describe_shutdown() (+7 more)

### Community 54 - "Doctor Health Checks"
Cohesion: 0.24
Nodes (15): Check, _check_chunker(), _check_corpus(), _check_langchain(), _check_llm(), _check_reranker(), _check_store(), Path (+7 more)

### Community 55 - "OpenAI-Compatible Chat Provider"
Cohesion: 0.14
Nodes (11): Chat model providers. Imported for registration side effects., _make_factory(), OpenAICompatibleChatModel, _parse_usage(), _Preset, Any, Chat provider for any OpenAI-compatible endpoint. One adapter covers OpenAI,…, Adapter over the `/v1/chat/completions` interface. (+3 more)

### Community 56 - "Parse Errors & Format Parsers"
Cohesion: 0.21
Nodes (16): ParseError, A source file could not be turned into text. Raised per file and caught by the…, parse_docx(), parse_html(), parse_pdf(), parse_text(), parse_xlsx(), ParsedContent (+8 more)

### Community 57 - "Chunk Size & Vector Dimension Decisions"
Cohesion: 0.14
Nodes (16): Chunk Size As The Highest-Leverage Knob, Vector Dimension Fixed In The DDL / DimensionMismatchError, Embedding Model Chosen Independently Of The Chat Model, nomic-embed-text (768 dimensions), fact_match, Container Injects Vector Width And Embedding Model Id, Lazy cached_property Container Construction, Registry And Composition Root Wiring (+8 more)

### Community 58 - "Filesystem Loader & Title Derivation"
Cohesion: 0.17
Nodes (13): _derive_title(), FilesystemLoader, Path, Use the first Markdown heading as the title, else the filename. Titles are…, Loads documents from a directory tree, one parser per format. The Phase 1…, Path, Regression: the corpus boundary is enforced by two defaults agreeing.…, test_filesystem_loader_ids_are_stable() (+5 more)

### Community 59 - "Persistent Trace Store"
Cohesion: 0.17
Nodes (7): Path, Record one completed trace. Never raises. A read-only filesystem, a full disk…, Completed traces, most recent first., Look up by full id, or by a unique prefix — ids get pasted by hand., Yield traces newest first, current file before rotated. Reads whole files…, A size-bounded, append-only log of completed traces. Two files: the one being…, TraceStore

### Community 60 - "Ingestion Logging & Trace Persistence"
Cohesion: 0.15
Nodes (11): Logger, The ingestion pipeline: documents in, embedded chunks in the store. Idempotent…, get_logger(), Traces that outlive the process that produced them. The in-memory recorder in…, _log_span(), Execution tracing: how a request actually spent its time. Structured logs…, Attach human text (a query, an answer, a chunk excerpt). Kept separate from…, Emit one completed span as a TRACE record. Guarded by `isEnabledFor` before… (+3 more)

### Community 61 - "Chat & Health Endpoints"
Cohesion: 0.18
Nodes (15): post, Request, chat(), _container(), health(), Liveness plus the active component set. Returning the resolved configuration…, Run retrieval only. Exposed as its own endpoint because retrieval quality is…, The trace for `trace_id`, if it is still in the buffer. Returned inline on… (+7 more)

### Community 62 - "Logging Documentation & ADR 0009"
Cohesion: 0.14
Nodes (12): Configuration, Coverage comes from the span bridge, Debugging workflows, Four properties that are load-bearing, Known limits, Levels, Logging, Logging and tracing are not the same thing (+4 more)

### Community 63 - "Graphify Graph Findings"
Cohesion: 0.20
Nodes (14): Dangling-Endpoint Edges Are Mostly Not a Defect, Fewer Nodes, More Edges, Rebuilding Needs the office and sql Extras, Graphify, A Test Double Was the Most Connected Node, docs/company Is the Corpus; docs/engineering Is Not, 34 of 193 Chunks Are Exact Duplicates, FAQ Split into 17 Topic Files (+6 more)

### Community 64 - "Whitespace Normalisation & Error Base"
Cohesion: 0.15
Nodes (11): Exception, normalize_whitespace(), Collapse runs of blank lines. Applied by loaders before chunking., AssistantError, Base class for every error raised by this package., Corpus ingestion: connectors, text extraction, and the chunk/embed/store…, Corpus connectors. A loader is any object with `load() ->…, Derive a stable id from a source URI. Hashed rather than slugified so the id is… (+3 more)

### Community 65 - "Add-on Tier Pricing & Discount Slabs"
Cohesion: 0.15
Nodes (13): Add-on Tier Pricing, Cost Parameters and Profit Margins (up to 4 costs, 2 margins), Per-Variant Quantity Range Evaluation, App-Created Discount Label, Best Discount Tier Across Multiple Collections, Combined Collection Quantity Discount Slabs, OSCP Support Channel (apps@oscprofessionals.com), Offer List Drag-and-Drop Ordering (+5 more)

### Community 66 - "Chunker Factories & Pipeline Wiring"
Cohesion: 0.23
Nodes (10): Protocol, _build_langchain_recursive(), _build_markdown(), register, Chunkers backed by `langchain-text-splitters`. **Why adopt a library here, of…, Chunker, Splits a document into retrievable units., ComponentConfig (+2 more)

### Community 67 - "Observability Entry & Trace Rendering"
Cohesion: 0.23
Nodes (11): Observability: tracing, persistence, and the rendering of traces. Three modules…, _details(), _label(), Rendering a trace for a human. Separate from `trace` because collection and…, Draw the trace as an indented waterfall. Bars are positioned by `offset_ms` and…, One line: id, name, duration, span count, outcome., The first few attributes, plus any error. Truncated on purpose: a waterfall is…, render_summary() (+3 more)

### Community 68 - "Experiment Profiles & Embedding Caveats"
Cohesion: 0.17
Nodes (12): 3072-Dimension Embedding Caveat, 384-Dimension Database Separation, BGE Asymmetric Query Prefix, cross_encoder Reranker (ms-marco-MiniLM-L-6-v2), local-only Experiment Profile, The cli.command Record, Instrument the Pipeline, Not the Adapter, Container — Composition Root and Lifecycle (+4 more)

### Community 69 - "Cart Discount & Order Limits"
Cohesion: 0.21
Nodes (12): Cart Discount, Order Limits, Row-Level Then Order-Level Discount Ordering, Row Level Discount, FEAT-04 Cart Level Discount (SCN-006, SCN-007), FEAT-05 Order Limits Min/Max (SCN-008, SCN-009), MOQ — Minimum Order Quantity (glossary), OSCP Wholesale B2B Pricing — Scenario Document (+4 more)

### Community 70 - "Offer Priority & Storefront Integration"
Cohesion: 0.20
Nodes (12): Priority of the Offers, Product and Collection Page Integration, Quick Order Form, Custom Price Grid App Block / App Embed, Theme Compatibility, Tiered Pricing (collection, product and variant level), FEAT-01 Quantity Break Pricing (SCN-001, SCN-002), FEAT-07 Quick / Bulk Order Form (SCN-011) (+4 more)

### Community 71 - "Ponytail Discipline & Evaluation Framework"
Cohesion: 0.18
Nodes (12): The ponytail: Comment Convention, Lazy at the Core, Strict at the Edges, Ponytail, Deterministic Metrics Gate CI; the LLM Judge Is Opt-In, Evaluation Framework, Frozen Prompts, Hybrid Retrieval with Reciprocal Rank Fusion, A Retrieval Change Ships With a Measured Improvement (+4 more)

### Community 72 - "Trace Sink & JSONL Parsing"
Cohesion: 0.18
Nodes (12): active_trace_store(), The store traces are being written to, if persistence is enabled., _parse_line(), Any, Parse one record, skipping anything malformed. A truncated final line is…, Rebuild a `Trace` from its serialised form. The inverse of `Trace.to_dict`, and…, trace_from_dict(), One format for the file and the HTTP body, so one parser serves both. (+4 more)

### Community 73 - "Voyage Embeddings"
Cohesion: 0.23
Nodes (5): BaseModel, Vector, Adapter over the Voyage AI embeddings endpoint., VoyageEmbeddingModel, VoyageOptions

### Community 74 - "The Logging System & Span Bridge"
Cohesion: 0.25
Nodes (11): Writing Is Off the Calling Thread, The Logging System, Logging and Tracing Answer Different Questions, The Span Bridge, trace_id Stamped on Every Log Record, TRACE Level (5), Rejected — Hand-Written Log Lines in Every Pipeline, Rejected — Replace the Trace Store With Logs (+3 more)

### Community 75 - "Local Embedding Model"
Cohesion: 0.22
Nodes (5): LocalEmbeddingModel, LocalEmbeddingOptions, BaseModel, Vector, Adapter over a `sentence-transformers` model loaded in-process.

### Community 76 - "Session Startup & Deduplication (ADR 0008)"
Cohesion: 0.31
Nodes (10): Session Startup Protocol, Session Startup Protocol (claude.md), ADR 0008 — Deduplicate by Source, Not by Content, content_hash (per-document change detection), Rejected: Deduplicate at Ingest, Source-Keyed Document Identity, Architecture Decision Records, ADRs Are Append-Only (+2 more)

### Community 77 - "ADR 0009 Structure"
Cohesion: 0.22
Nodes (10): ADR 0009 — Persistent Logging on the Standard Library, Fed by the Span Stream, Alternatives considered, Consequences, Context, Decision, Everything Else Is Stdlib, The span bridge is the load-bearing decision, TRACE is off by default (+2 more)

### Community 78 - "Trace & Status Endpoints"
Cohesion: 0.22
Nodes (9): get, get_trace(), list_traces(), What is currently indexed. Separate from `/health` because it queries the…, Recent execution traces, most recent first., One execution trace in full, by id or unique prefix., status(), IndexStatusBody (+1 more)

### Community 79 - "HTML Parser"
Cohesion: 0.20
Nodes (5): HTMLParser, _HtmlTextExtractor, Any, Collects visible text, discarding markup and non-content elements., The collected text, with each block element on its own line.

### Community 80 - "OpenAI-Compatible Embeddings"
Cohesion: 0.29
Nodes (4): OpenAICompatibleEmbeddingModel, Vector, Release the underlying HTTP client. `Container.shutdown()` probes every…, Adapter over the `/v1/embeddings` interface.

### Community 81 - "Doctor Command Tests"
Cohesion: 0.20
Nodes (10): Path, A directory of .pptx looks identical to an empty corpus in the sync report., Construction alone passes with the model unpulled or the credential expired., A failing provider must be named on one line, not raised as a traceback., test_doctor_can_skip_the_live_calls(), test_doctor_makes_live_calls_by_default(), test_doctor_passes_when_every_component_is_reachable(), test_doctor_reports_a_broken_component_and_exits_non_zero() (+2 more)

### Community 82 - "Draft Order Processing"
Cohesion: 0.22
Nodes (9): Shopify Coupon Applied After Tier Discount, Draft Order Processing, 15-Minute Invoice Reuse Window, oscp-order-processing Order Tag, Server-Side Wholesale Price Validation, FEAT-10 Auto Order Tagging (SCN-014), Metafield (glossary), EC-07 Cart Discount Plus Shopify Native Discount Code (+1 more)

### Community 83 - "Chat Web UI"
Cohesion: 0.31
Nodes (9): Complete event is authoritative, el (element factory), Grounded answer / abstention contract, Health check status banner, OSC Knowledge Assistant Web UI, Conversation history deliberately not sent, renderSources, SSE chat stream protocol (sources/delta/citation/complete/error) (+1 more)

### Community 84 - "Trace Listing CLI"
Cohesion: 0.25
Nodes (9): _fetch_traces(), _inspector(), List recent execution traces, most recent first. Read from the persisted trace…, traces(), _traces_from(), fail(), Report an operator-facing error and exit non-zero., Read-only introspection of what a store currently holds. Kept **separate from… (+1 more)

### Community 85 - "Observability Installation & Isolation"
Cohesion: 0.22
Nodes (9): configure_observability(), Path, Install the whole observability stack. Safe to call more than once. Persistence…, Install a destination for completed traces, or `None` to remove one. A callable…, set_trace_sink(), _isolate_observability(), MonkeyPatch, Path (+1 more)

### Community 86 - "B2B Registration, Export & Notifications"
Cohesion: 0.32
Nodes (8): CSV Export and Bulk Import of Variant Rules, Email Notification Setup (three templates), B2B Registration Form, FEAT-06 B2B Registration Form (SCN-010), FEAT-09 Bulk CSV Import/Export (SCN-013), FEAT-12 Personalised Email Notifications (SCN-016), EC-14 CSV Import Conflicts With Existing Rules, FA-09 CSV Bulk Import / Export

### Community 87 - "Scenario Acceptance Criteria Bank"
Cohesion: 0.43
Nodes (8): Acceptance Criteria Bank (AC-01..AC-19), FA-01 Tiered / Volume Pricing, FA-03 Fixed Price Rules, FA-05 B2B Registration Form, FA-06 Quick Order Form, FA-10 Manual Order Support, Merchant Archetypes Reference (MA-01..MA-07), OSCP Wholesale B2B — Scenario Master (SCN-001..SCN-010)

### Community 88 - "CLI Test Environment Doubles"
Cohesion: 0.25
Nodes (8): MonkeyPatch, fixture, Point the CLI at in-process doubles through configuration alone. Which is the…, `AssistantError` names a problem the operator must fix; frames bury it., The trace names the stage that raised and what every earlier stage did., _stub_environment(), test_a_failure_inside_a_stage_prints_the_trace(), test_an_operator_error_is_a_message_not_a_traceback()

### Community 89 - "Startup Banner & Lifecycle"
Cohesion: 0.29
Nodes (7): describe_startup(), Human-facing startup and shutdown reporting for the service. The structured…, Print where the service is listening and what it is running. Failures are…, Conditions worth telling a developer about before their first request. Returned…, startup_notes(), A chat UI on an unauthenticated service is the state most easily mistaken for…, test_a_non_development_environment_is_called_out()

### Community 91 - "Gemini Embeddings"
Cohesion: 0.39
Nodes (3): GeminiEmbeddingModel, Vector, Adapter over `google-genai`'s embedding interface.

### Community 92 - "Noop Reranker & Evaluation Corpus"
Cohesion: 0.25
Nodes (6): NoopReranker, Truncates the candidate list without reordering it., corpus(), fixture, A three-document corpus with `relative_path` set, as the loader would., retrieval()

### Community 93 - "Citations & Native Citation Model"
Cohesion: 0.29
Nodes (4): Citation, A reference from the answer back to the material that supports it. `index` is…, NativeCitationChatModel, A chat model that resolves citations itself, as Anthropic does.

### Community 94 - "Default Configuration Profile"
Cohesion: 0.33
Nodes (7): chunking: configuration block, include_usage_in_stream, Default Profile (fully local), logging: configuration block, reasoning_effort: none, reranker: noop, retrieval: configuration block

### Community 95 - "Observability Config & Rationale"
Cohesion: 0.43
Nodes (7): observability: configuration block, capture_text Privacy Seam, Why a JSONL File (alternatives rejected), Observability Subsystem, render.py (waterfall renderer), store.py (append-only JSONL trace log), trace.py (context-var span tree)

### Community 96 - "Extra Fee, Free Gift & Customer Tags"
Cohesion: 0.33
Nodes (7): Extra Fee, Free Gift, Customer Tag (glossary), FEAT-02 Customer Tag Tier Pricing (SCN-003, SCN-004), FEAT-11 Hide Shipping Methods (SCN-015), SCN-X01 Customer-Level Fixed Price per SKU (out of scope), Customer Group Matrix (All / Logged In / Wholesale / VIP)

### Community 97 - "Markets Pricing & Tax Display"
Cohesion: 0.29
Nodes (7): Market-Based Offers, Tax Display, FEAT-03 Markets-Based Pricing (SCN-005), FEAT-08 Tax Display by Country (SCN-012), Shopify Market (glossary), FA-07 Multi-Currency / Markets, FA-08 Tax Display (PDP Widget)

### Community 98 - "Trace Persistence Decision (ADR 0004)"
Cohesion: 0.29
Nodes (7): Every Case Records Its Trace Id, ADR 0004 — Persist Traces To A Bounded JSONL File, Auto-Explain On Failure, Bounded Means Lossy — Not An Audit Log, OpenTelemetry Exporter Deferred, Span Stays OTel-Shaped, Rejected: A traces Table In PostgreSQL, One Database Is One Failure Domain

### Community 99 - "ADR 0008 Content Deduplication"
Cohesion: 0.33
Nodes (5): ADR 0008 — Ingestion deduplicates by source, not by content, Alternatives considered, Consequences, Context, Decision

### Community 100 - "Evaluation Run Comparison"
Cohesion: 0.33
Nodes (5): compare(), Any, The on-disk shape. Stable, because baselines are compared against it., Metrics present in both runs, as (name, baseline, current). Only the…, test_compare_only_diffs_metrics_present_in_both_runs()

### Community 101 - "Abstention Policy & Output Streams"
Cohesion: 0.40
Nodes (5): The Console Can Be Quieter Than the File, Two Abstention Mechanisms, One Measured, Architectural Abstention Policy, Human Output on stderr, Machine Output on stdout, The Empty-Index Startup Note

### Community 102 - "Golden Set Curation Rules"
Cohesion: 0.40
Nodes (5): Abstention case set (must_abstain), expected_facts curation rule, OSC Golden Set (86 cases), OSCP Wholesale B2B FAQ corpus (17 topic files), Questions phrased as a merchant would ask them

### Community 103 - "Inspection Payloads & Redaction"
Cohesion: 0.40
Nodes (5): _document_payload(), Any, Blank anything whose key suggests a credential. Name-based rather than value-…, _redact(), _statistics_payload()

### Community 104 - "Judge Verdict Parsing"
Cohesion: 0.50
Nodes (3): _parse_verdict(), Read a one-word verdict out of whatever the model actually returned. Substring…, Return True, False, or None when the judge could not be reached. `None` rather…

## Ambiguous Edges - Review These
- `Query Rewriting (off by default)` → `No Authentication, Rate Limiting Or Concurrency Bound`  [AMBIGUOUS]
  docs/engineering/architecture/retrieval.md · relation: conceptually_related_to

## Knowledge Gaps
- **80 isolated node(s):** `osc-assistant`, `Logging and tracing are not the same thing`, `Where logs go`, `Four properties that are load-bearing`, `Coverage comes from the span bridge` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Query Rewriting (off by default)` and `No Authentication, Rate Limiting Or Concurrency Bound`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Document` connect `Ingestion Pipeline & Loaders` to `LangChain Bridges & Splitters`, `Answer Generation & Faithfulness Judge`, `pgvector Store & Integration Tests`, `Error Hierarchy & Embedding Providers`, `Citation Parsing & Gemini Chat`, `Composition Root & Settings Models`, `In-Memory Vector Store`, `Chunker Registration & Options`, `Protocol Seams & Embedding Errors`, `Store Construction & Embedding Calls`, `Shared Test Fixtures & Retrieval Tests`, `Stub Chat Model & Answerer Tests`, `Recursive & Markdown Splitting`, `Server Lifecycle Tests`, `Reranker Protocol & Provider Registration`, `Provider Errors & ChatModel Protocol`, `VectorStore Errors & Inspection`, `Chunk Types & Document Chunks`, `Fusion & Store Statistics`, `Filesystem Loader & Title Derivation`, `Ingestion Logging & Trace Persistence`, `Whitespace Normalisation & Error Base`, `Chunker Factories & Pipeline Wiring`, `Trace Listing CLI`, `Noop Reranker & Evaluation Corpus`, `Citations & Native Citation Model`, `Content Hashing`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `Citation Parsing & Gemini Chat` to `LangChain Bridges & Splitters`, `Answer Generation & Faithfulness Judge`, `Error Hierarchy & Embedding Providers`, `Composition Root & Settings Models`, `Protocol Seams & Embedding Errors`, `Store Construction & Embedding Calls`, `Grounded Prompt & LangChain Chat`, `Anthropic Adapter & Retrieval Pipeline`, `Shared Test Fixtures & Retrieval Tests`, `Stub Chat Model & Answerer Tests`, `Reranker Protocol & Provider Registration`, `Provider Errors & ChatModel Protocol`, `Citation Grounding & Reasoning Models`, `Doctor Health Checks`, `OpenAI-Compatible Chat Provider`, `Chunker Factories & Pipeline Wiring`, `Trace Listing CLI`, `Citations & Native Citation Model`, `Judge Verdict Parsing`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `StubEmbeddingModel` connect `Shared Test Fixtures & Retrieval Tests` to `Golden Set Loading & Evaluation Tests`, `Server Lifecycle Tests`, `pgvector Store & Integration Tests`, `Citation Parsing & Gemini Chat`, `Ingestion Pipeline & Loaders`, `Provider Errors & ChatModel Protocol`, `Composition Root & Settings Models`, `In-Memory Vector Store`, `Chunker Registration & Options`, `Noop Reranker & Evaluation Corpus`, `Citations & Native Citation Model`, `Stub Chat Model & Answerer Tests`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MemoryVectorStore` (e.g. with `FailingChatModel` and `NativeCitationChatModel`) actually correct?**
  _`MemoryVectorStore` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Document` (e.g. with `ChatModel` and `Chunker`) actually correct?**
  _`Document` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `StubEmbeddingModel` (e.g. with `MemoryVectorStore` and `ChatRequest`) actually correct?**
  _`StubEmbeddingModel` has 12 INFERRED edges - model-reasoned connections that need verification._