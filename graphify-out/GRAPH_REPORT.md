# Graph Report - .  (2026-08-05)

## Corpus Check
- 147 files · ~147,249 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1981 nodes · 4624 edges · 114 communities (94 shown, 20 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 503 edges (avg confidence: 0.72)
- Token cost: 358,214 input · 31,151 output

## Community Hubs (Navigation)
- CLI Commands — ask, ingest, search
- HTTP API Layer
- Error Hierarchy & Protocol Seams
- Evaluation CLI Command
- Faithfulness Judge & Answer Events
- Ingestion Pipeline & Loaders
- Rank Fusion & Source Rendering
- Container Lifecycle
- pgvector Store Interface
- Server Lifecycle & Startup Notes
- Settings Loading & YAML Profiles
- HTTP Layer Tests
- LangChain Chat Bridge
- Tracing & Retrieval Instrumentation
- Grounding & OpenAI-Compatible Chat
- Recursive Chunker
- Golden Set Schema & Validation
- Settings Schema
- Trace Store Tests
- Configuration Errors & Gemini Embeddings
- LangChain Text Splitters
- Chat Request & Response Types
- In-Memory Vector Store
- ADRs — Protocol & LangChain Decisions
- Markdown Chunker & LangChain Tests
- Citation Parsing & Gemini Chat
- Anthropic Chat Adapter
- Evaluator & Answerer Composition
- Trace Fetching & Persistence
- Golden Set Loading & Evaluation Tests
- Chunking Strategies & Ingestion Rules
- Parser Tests & Format Invariants
- Stub Embedding Model
- Evaluation Metrics & CI Gate
- Chunker Registration
- Execution Tracing Core
- Outbound LangChain Retriever
- Stub Chat Model & Answerer Tests
- The Five Protocol Seams
- AssistantError Base & Loaders
- Observability Composition & Rendering
- CLI Tests
- Embedding & Chunk-Size Decisions
- Retrieval Metrics
- LangChain Embedding Bridge
- pgvector Search & Migrations
- Text Extraction Parsers
- Vector Store Registration
- Startup Banner & Composition Root
- VectorStore Protocol
- Persistent Tracing Design (ADR 0004)
- Observability & API Weak Points
- Hybrid Retrieval & RRF (ADR 0003)
- Filesystem Loader & Corpus Boundary
- Memory Store Search
- Golden Set Curation & Corpus Rules
- Span Context Management
- Add-on Tier Pricing & Collection Slabs
- Experiment Profiles & Embedding Caveats
- Chunking & Model Config Decisions
- Default Profile & Retrieval Config
- Cart Discount & Order Limits
- Offer Priority & Theme Integration
- Golden Set & Config Layering
- ChatModel Protocol
- Retrieval Pipeline
- Trace Store
- Store Inspector
- Voyage Embeddings
- Evaluation Findings & Milestones
- ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split...
- EmbeddedChunk
- OpenAICompatibleEmbeddingModel
- conftest.py
- Path
- Draft Order Processing
- Chat form submit handler
- FEAT-06 B2B Registration Form (SCN-010)
- Four Test Tiers
- OSCP Wholesale B2B — Scenario Master (SCN-001..SCN-010)
- _HtmlTextExtractor
- GeminiEmbeddingModel
- LocalEmbeddingModel
- CrossEncoderReranker
- _stub_environment()
- FEAT-02 Customer Tag Tier Pricing (SCN-003, SCN-004)
- FEAT-03 Markets-Based Pricing (SCN-005)
- Operational Tooling (./osc CLI)
- Observability Layer (trace / store / render)
- Session Startup Checklist
- IndexStatistics
- DimensionMismatchError
- OSCRetriever()
- NoopReranker
- .register()
- generation/__init__.py
- 001_init.sql
- content_hash()
- Groq + Voyage Experiment Profile
- pgvector Image Tag Pinning Intent
- osc
- integrations/__init__.py
- test_config_redacts_credentials_by_default()
- test_ask_explain_prints_the_execution_trace()
- test_traces_are_readable_after_the_command_that_made_them...
- test_trace_with_no_id_expands_the_most_recent()
- test_traces_can_be_filtered_by_name()
- test_trace_reports_an_unreachable_service_actionably()
- test_help_groups_commands_by_purpose()
- test_first_turn_is_not_rewritten()
- _stub_providers()
- Hosted Models Lift the Prompt Budget
- osc-assistant

## God Nodes (most connected - your core abstractions)
1. `MemoryVectorStore` - 72 edges
2. `Document` - 70 edges
3. `StubEmbeddingModel` - 69 edges
4. `ComponentConfig` - 64 edges
5. `Container` - 60 edges
6. `ChatRequest` - 59 edges
7. `StubChatModel` - 44 edges
8. `PgVectorStore` - 43 edges
9. `ScoredChunk` - 40 edges
10. `Settings` - 38 edges

## Surprising Connections (you probably didn't know these)
- `FEAT-01 Quantity Break Pricing (SCN-001, SCN-002)` --semantically_similar_to--> `Add-on Tier Pricing`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_B2B_Scenario_Document-1_cb06f24b.md → docs/company/faq/add-on-tier-pricing.md
- `FEAT-04 Cart Level Discount (SCN-006, SCN-007)` --semantically_similar_to--> `Cart Discount`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_B2B_Scenario_Document-1_cb06f24b.md → docs/company/faq/cart-discount.md
- `FA-10 Manual Order Support` --semantically_similar_to--> `Draft Order Processing`  [INFERRED] [semantically similar]
  graphify-out/converted/OSCP_Wholesale_B2B_Scenario_Templates_0ba70067.md → docs/company/faq/draft-order.md
- `OSC Engineering Handbook (claude.md)` --semantically_similar_to--> `OSC Engineering Handbook (AGENTS.md)`  [INFERRED] [semantically similar]
  claude.md → AGENTS.md
- `Quantity Clubbed for Variants of a Product` --semantically_similar_to--> `Per-Variant Quantity Range Evaluation`  [INFERRED] [semantically similar]
  graphify-out/converted/Use Cases _ OSCP Wholesale B2B App - Quantity Clubbed for Product Asset 2025_51fc9cac.md → docs/company/faq/add-on-tier-pricing.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Streamed grounded answer flow in the web client** — src_osc_assistant_api_static_index_submithandler, src_osc_assistant_api_static_index_rendersources, src_osc_assistant_api_static_index_ssestreamprotocol, src_osc_assistant_api_static_index_completeeventauthority, src_osc_assistant_api_static_index_groundedanswercontract [EXTRACTED 1.00]
- **Tier price precedence resolution across variant, product and collection scopes** — docs_company_faq_priority_of_the_offers_offer_priority, docs_company_faq_priority_of_the_offers_offer_list_ordering, docs_company_faq_tiered_pricing_guide_tiered_pricing, docs_company_faq_combined_collection_quantity_discount_slabs_best_tier_across_collections, graphify_out_converted_oscp_wholesale_b2b_scenario_templates_0ba70067_ec_01_multiple_tag_discount_conflict [INFERRED 0.85]
- **B2B account onboarding: registration, notification, approval, tag-gated pricing** — docs_company_faq_registration_form_registration_form, docs_company_faq_registration_form_email_notification_setup, graphify_out_converted_oscp_b2b_scenario_document_1_cb06f24b_feat_06_b2b_registration_form, graphify_out_converted_oscp_b2b_scenario_document_1_cb06f24b_feat_12_email_notifications, graphify_out_converted_oscp_wholesale_b2b_scenario_templates_0ba70067_fa_05_b2b_registration_form [INFERRED 0.85]
- **Delivering the wholesale price at checkout via Draft Orders** — docs_company_faq_draft_order_draft_order_processing, docs_company_faq_draft_order_server_side_price_validation, docs_company_faq_draft_order_invoice_reuse_window, docs_company_faq_draft_order_oscp_order_processing_tag, docs_company_faq_draft_order_coupon_after_tier_discount_ordering [EXTRACTED 1.00]
- **The Five Swappability Protocols** — docs_engineering_architecture_provider_architecture_chatmodel_protocol, docs_engineering_architecture_provider_architecture_embeddingmodel_protocol, docs_engineering_architecture_provider_architecture_vectorstore_protocol, docs_engineering_architecture_provider_architecture_reranker_protocol, docs_engineering_architecture_provider_architecture_chunker_protocol, docs_engineering_architecture_provider_architecture_storeinspector_protocol [EXTRACTED 1.00]
- **The Measured-Improvement Discipline** — docs_engineering_decisions_0006_chunking_strategy_measured_improvement_rule, docs_engineering_architecture_evaluation_evaluation_harness, docs_engineering_architecture_evaluation_committed_baselines, docs_engineering_architecture_chunking_and_embeddings_recursive_chunker, docs_engineering_architecture_retrieval_cross_encoder_reranking, docs_engineering_architecture_retrieval_query_rewriting [INFERRED 0.95]
- **Enforcing The Corpus Boundary** — docs_engineering_architecture_knowledge_corpus_corpus_boundary_rule, docs_engineering_readme_corpus_exclusion_rule, docs_engineering_decisions_0007_knowledge_corpus_layout_exclusion_list_rejected, docs_engineering_architecture_testing_corpus_isolation_rule, docs_engineering_architecture_knowledge_corpus_access_control_uniformity [INFERRED 0.95]
- **The protocol seam layer: five Protocols, one optional inspector, and the wiring that keeps providers out of business logic** — project_status_five_seams, project_status_storeinspector, project_status_vendor_agnosticism, project_status_registry_wiring, project_status_composition_root [EXTRACTED 1.00]
- **Measure-before-you-change loop: the rule, the harness, the golden set, the baseline and the commands that enforce it** — agents_measurement_rules, project_status_evaluation_framework, evaluation_golden_set_goldenset, project_status_measured_baseline, readme_evaluation, config_default_reranker_noop [INFERRED 0.85]
- **Scoped LangChain adoption: bridge providers, heading-aware splitting, the experiment profile and the citation cost it carries** — project_status_langchain_integration, config_experiments_langchain_bridge_profile, config_experiments_langchain_bridge_markdown_chunking, readme_experiment_profiles, project_status_citation_strength_gap [INFERRED 0.85]

## Communities (114 total, 20 thin omitted)

### Community 0 - "CLI Commands — ask, ingest, search"
Cohesion: 0.06
Nodes (71): ExplainOption, _answer_payload(), ask(), ingest(), _print_answer(), Argument, command, help (+63 more)

### Community 1 - "HTTP API Layer"
Cohesion: 0.06
Nodes (61): FastAPI, get, Logger, LogRecord, post, Request, chat(), _container() (+53 more)

### Community 2 - "Error Hierarchy & Protocol Seams"
Cohesion: 0.06
Nodes (49): Exception hierarchy for the assistant. A single root (`AssistantError`) lets…, A component was requested by a name that is not registered., UnknownComponentError, EmbeddingModel, The five seams of the system. Every swappable component is defined here as a…, A second-stage relevance model applied to retrieval candidates., A text embedding model. Document and query embedding are separate methods…, Vector width. Must match the vector store's configured dimension. (+41 more)

### Community 3 - "Evaluation CLI Command"
Cohesion: 0.08
Nodes (41): min, _assert_golden_set_is_resolvable(), _default_output(), _enforce_thresholds(), eval(), _execute(), _print_comparison(), _print_report() (+33 more)

### Community 4 - "Faithfulness Judge & Answer Events"
Cohesion: 0.07
Nodes (33): AnswerEvent, _parse_verdict(), LLM-as-judge faithfulness scoring. Faithfulness asks whether every claim in an…, Read a one-word verdict out of whatever the model actually returned. Substring…, Return True, False, or None when the judge could not be reached. `None` rather…, _annotate_abstention(), _annotate_generation(), AnswerComplete (+25 more)

### Community 5 - "Ingestion Pipeline & Loaders"
Cohesion: 0.09
Nodes (38): InMemoryLoader, Serves a fixed list of documents. Used by tests and the evaluation harness., IngestionPipeline, Chunk, embed and store one document. Each of the three stages gets its own…, Delete indexed documents that the source no longer offers. `keep` is every…, Chunks, embeds and stores documents., Sync `documents` into the store. Args: documents: The full current contents of…, Document (+30 more)

### Community 6 - "Rank Fusion & Source Rendering"
Cohesion: 0.08
Nodes (39): Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…, Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…, reciprocal_rank_fusion(), _escape(), Escape the characters that would otherwise break out of an XML-ish attribute., Render sources as a delimited block for inclusion in a prompt. The delimiter…, render_sources(), Render the results as grounding material for the model. (+31 more)

### Community 7 - "Container Lifecycle"
Cohesion: 0.08
Nodes (32): Self, Container, Release everything that was actually built. Only components whose…, Builds and owns the application's components., _build_corpus(), corpus(), indexed(), fixture (+24 more)

### Community 8 - "pgvector Store Interface"
Cohesion: 0.08
Nodes (31): PgVectorOptions, PgVectorStore, BaseModel, Adapter over PostgreSQL with the pgvector extension., The partition this store reads and writes. Every query is scoped to it., Integration tests for the PostgreSQL store. Skipped unless `OSC_TEST_DSN`…, setup() ran the migrations; running them again must be a no-op., Chunk ids incorporate content, so an edit yields new ids. Without the delete… (+23 more)

### Community 9 - "Server Lifecycle & Startup Notes"
Cohesion: 0.09
Nodes (31): Conditions worth telling a developer about before their first request. Returned…, startup_notes(), exploding_client(), _ExplodingChatModel, StreamEvent, TestClient, Startup, shutdown and in-flight failure behaviour of the service. These cover…, A condition worth interrupting a developer for belongs in the log as well. (+23 more)

### Community 10 - "Settings Loading & YAML Profiles"
Cohesion: 0.10
Nodes (30): BaseSettings, PydanticBaseSettingsSource, load_settings(), Any, Lowest-precedence source reading a YAML profile. The profile path comes from…, Build settings, applying `overrides` at the highest precedence., _YamlProfileSource, _isolate_environment() (+22 more)

### Community 11 - "HTTP Layer Tests"
Cohesion: 0.09
Nodes (32): client(), _development_client(), _parse_sse(), fixture, parametrize, TestClient, HTTP layer tests. These run the real application — real container, real…, Validation happens at the trust boundary, before any provider is touched. (+24 more)

### Community 12 - "LangChain Chat Bridge"
Cohesion: 0.10
Nodes (26): compose_grounded_system(), Fold the system prompt, citation instruction and sources into one string. Used…, _build(), _instantiate(), LangChainChatModel, LangChainChatOptions, _parse_usage(), Any (+18 more)

### Community 13 - "Tracing & Retrieval Instrumentation"
Cohesion: 0.10
Nodes (30): Expand one execution trace into a stage-by-stage waterfall. With no id this…, trace(), annotate(), configure_tracing(), Attach attributes to the innermost active span, if there is one. The…, Install tracing configuration. Safe to call more than once., Retrieve the chunks most relevant to `question`., fixture (+22 more)

### Community 14 - "Grounding & OpenAI-Compatible Chat"
Cohesion: 0.09
Nodes (24): Grounding and citation handling for providers without native citation support.…, Remove a leading `<think>` block from a reasoning model's answer. Ollama…, Fail loudly when the model produced no answer text. An empty completion…, require_answer(), strip_reasoning(), _make_factory(), OpenAICompatibleChatModel, _parse_usage() (+16 more)

### Community 15 - "Recursive Chunker"
Cohesion: 0.14
Nodes (27): ChunkerOptions, BaseModel, Splits on the coarsest separator that keeps chunks under the target size. Falls…, RecursiveChunker, _document(), Chunking tests. Chunk id stability is the load-bearing property here: ingestion…, Chunk text is quoted back to users as citation evidence, so the chunker must…, Ingestion skips unchanged documents by hash; ids must not drift. (+19 more)

### Community 16 - "Golden Set Schema & Validation"
Cohesion: 0.11
Nodes (21): field_validator, model_validator, document_key(), GoldenCase, BaseModel, The identity a golden set refers to a retrieved chunk's document by.…, One question and what a correct system does with it., Measurement for the retrieval and generation stack. The project's rule is that… (+13 more)

### Community 17 - "Settings Schema"
Cohesion: 0.11
Nodes (20): OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…, ChunkingSettings, DatabaseSettings, GenerationSettings, ObservabilitySettings, BaseModel, Configuration. Layered, highest precedence first: process environment, then…, How much the system records about its own execution. Defaults are chosen for a… (+12 more)

### Community 18 - "Trace Store Tests"
Cohesion: 0.15
Nodes (29): active_trace_store(), The store traces are being written to, if persistence is enabled., _isolated_tracing(), fixture, Path, Persisted trace tests. The store exists so a one-shot CLI command's trace…, Discarding everything at the moment the limit is hit is reliably the moment…, A truncated final line is expected: the writer may have been killed. (+21 more)

### Community 19 - "Configuration Errors & Gemini Embeddings"
Cohesion: 0.09
Nodes (23): Embeddings, ConfigurationError, MissingDependencyError, The system is misconfigured and cannot start or serve a request. Raised for…, A provider was selected but its optional dependency is not installed., GeminiEmbeddingOptions, BaseModel, _instantiate() (+15 more)

### Community 20 - "LangChain Text Splitters"
Cohesion: 0.10
Nodes (20): _build_langchain_recursive(), _build_markdown(), _heading_path(), LangChainRecursiveChunker, Any, register, Chunkers backed by `langchain-text-splitters`. **Why adopt a library here, of…, Join whichever heading levels are present into a readable path. (+12 more)

### Community 21 - "Chat Request & Response Types"
Cohesion: 0.13
Nodes (16): Generate a complete response., ChatRequest, ChatResponse, Citation, CitationDelta, A reference from the answer back to the material that supports it. `index` is…, A provider-neutral generation request. `sources`, when present, is grounding…, An incremental fragment of the answer. (+8 more)

### Community 22 - "In-Memory Vector Store"
Cohesion: 0.10
Nodes (17): MemoryVectorStore, A dictionary-backed `VectorStore`., Replace a document and its chunks. Atomic by construction: the vectors are…, Store inspection tests. `StoreInspector` is what the operational commands are…, The last step of verifying a citation: the exact text the model was shown., The protocol is optional; a store that cannot support it is still a store. Both…, The point of measuring is comparing against the configured target. A…, test_a_chunk_can_be_fetched_by_id() (+9 more)

### Community 23 - "ADRs — Protocol & LangChain Decisions"
Cohesion: 0.11
Nodes (27): Parsers Extract And Never Rewrite, LLM-As-Judge Faithfulness (opt-in), Zheng et al., Judging LLM-as-a-Judge (NeurIPS 2023), Machine Output On stdout, Human Output On stderr, Structured Logging On stdlib logging, ADR 0001 — Five Protocols As The Swappability Seams, Rejected: Abstract Base Classes And Framework Abstractions, Provider-Specific Tuning Lives In Untyped options (+19 more)

### Community 24 - "Markdown Chunker & LangChain Tests"
Cohesion: 0.14
Nodes (24): LangChainChunkerOptions, MarkdownChunker, Heading-aware splitting: structure first, then size. Two passes, because either…, `ChunkerOptions` plus the settings only the LangChain splitters expose., _document(), parametrize, LangChain integration tests. Three surfaces, three concerns: * **Chunkers** —…, Chunk text is quoted back as citation evidence, so no character may be… (+16 more)

### Community 25 - "Citation Parsing & Gemini Chat"
Cohesion: 0.13
Nodes (18): ProviderError, An upstream provider (LLM, embeddings, reranker) failed., parse_marker_citations(), Extract citations from `[n]` markers in `text`. Markers referring to a source…, The collected text, with each block element on its own line., _build(), _build_contents(), _finish_reason() (+10 more)

### Community 26 - "Anthropic Chat Adapter"
Cohesion: 0.11
Nodes (18): AnthropicChatModel, AnthropicOptions, _build(), _build_messages(), _last_user_index(), _parse_content(), _parse_usage(), Any (+10 more)

### Community 27 - "Evaluator & Answerer Composition"
Cohesion: 0.18
Nodes (21): FaithfulnessJudge, Scores one answer against the passages it was generated from., Evaluator, Runs a golden set and scores it. Takes the pipelines rather than the…, Answerer, Answers a question against the indexed corpus., Composes rewriting, search and reranking into one call., RetrievalPipeline (+13 more)

### Community 28 - "Trace Fetching & Persistence"
Cohesion: 0.12
Nodes (19): _fetch_traces(), _traces_from(), fail(), Report an operator-facing error and exit non-zero., _parse_line(), Any, Traces that outlive the process that produced them. The in-memory recorder in…, Look up by full id, or by a unique prefix — ids get pasted by hand. (+11 more)

### Community 29 - "Golden Set Loading & Evaluation Tests"
Cohesion: 0.14
Nodes (16): load_golden_set(), Path, Read and validate a golden set file. Raises: EvaluationError: The file is…, parametrize, Path, Evaluation harness tests. The harness is the instrument every future retrieval…, test_a_missing_golden_set_names_the_file(), test_a_valid_golden_set_loads() (+8 more)

### Community 30 - "Chunking Strategies & Ingestion Rules"
Cohesion: 0.12
Nodes (24): Chunk Denormalises Title And Source URI, Shared Chunk Id Helper And Idempotent Ingestion, Chunking And Embedding Pipeline, EmbeddedChunk Carries Its Embedding Model Id, fixed Chunking Strategy, langchain_recursive Chunking Strategy, markdown Chunking Strategy, Unparseable Files Are Recorded As Failures, Not Deleted (+16 more)

### Community 31 - "Parser Tests & Format Invariants"
Cohesion: 0.15
Nodes (22): parse(), Extract `path` using the parser registered for its extension. Raises:…, Path, Text extraction and multi-format loading tests. Two properties are load-bearing…, A spreadsheet's meaning is two-dimensional; retrieval is not. The row is the…, A page-image PDF parses cleanly and yields nothing. Indexing an empty document…, Provenance is denormalised onto every chunk, so it has to be right here., The invariant that makes a citation quotable: text in equals text out. (+14 more)

### Community 32 - "Stub Embedding Model"
Cohesion: 0.15
Nodes (17): Vector, A deterministic bag-of-words embedder. Hashes each token into a fixed number of…, StubEmbeddingModel, _pipeline(), parametrize, Retrieval tests, including the vector store contract. `test_store_contract`…, Regression: the threshold must not be measured against reranker output. A…, This is what triggers abstention rather than a guessed answer. (+9 more)

### Community 33 - "Evaluation Metrics & CI Gate"
Cohesion: 0.12
Nodes (23): An Absent Metric Is Not A Zero Metric, abstention_accuracy, CI Gate via --fail-under, citation_coverage / citation_precision, Committed Baselines, Configuration Travels With The Numbers, Evaluation Harness, groundedness (+15 more)

### Community 34 - "Chunker Registration"
Cohesion: 0.13
Nodes (18): Chunking strategies. Imported for registration side effects., _build_fixed(), _build_recursive(), _chunk_id(), FixedSizeChunker, _merge(), normalize_whitespace(), Any (+10 more)

### Community 35 - "Execution Tracing Core"
Cohesion: 0.10
Nodes (14): annotate_text(), current_trace_id(), Execution tracing: how a request actually spent its time. Structured logs…, Attach human text (a query, an answer, a chunk excerpt). Kept separate from…, A bounded ring of recent traces, for `osc-assistant trace` and `/api/traces`.…, Look up by full id, or by a unique prefix — trace ids are pasted by hand., The active trace id, or `""` when nothing is tracing. Returned to clients and…, Attach human text to the innermost active span, honouring `capture_text`. (+6 more)

### Community 36 - "Outbound LangChain Retriever"
Cohesion: 0.10
Nodes (13): LangChainDocument, Exposing OSC to LangChain, rather than the other way round. Every other…, Translate one retrieval hit into a LangChain document. The score and the match…, to_langchain_document(), Vector, Lexical search. Return `[]` if the store has no lexical index., Combined lexical and vector search, fused into a single ranking., Return the `top_k` most relevant candidates, most relevant first. (+5 more)

### Community 37 - "Stub Chat Model & Answerer Tests"
Cohesion: 0.18
Nodes (18): A chat model that returns a scripted reply. `supports_citations` is False, so…, StubChatModel, _answerer(), Answer generation tests. The abstention policy is the system's main defence…, Both citation paths must produce the same shape for downstream code., The complete event is authoritative: clients discard streamed text when it…, Generating from nothing is guessing, so the model is never invoked., test_citation_requirement_can_be_relaxed() (+10 more)

### Community 38 - "The Five Protocol Seams"
Cohesion: 0.12
Nodes (20): Business Logic Imports protocols And types Only, integrations/ May Import The Core; The Core May Never Import integrations/, Module Map, ChatModel Protocol, EmbeddingModel Protocol, The Five Protocol Seams, PEP 544 — Structural Subtyping, Reranker Protocol (+12 more)

### Community 39 - "AssistantError Base & Loaders"
Cohesion: 0.12
Nodes (14): Exception, AssistantError, Base class for every error raised by this package., Corpus ingestion: connectors, text extraction, and the chunk/embed/store…, _derive_title(), Path, Corpus connectors. A loader is any object with `load() ->…, Use the first Markdown heading as the title, else the filename. Titles are… (+6 more)

### Community 40 - "Observability Composition & Rendering"
Cohesion: 0.14
Nodes (18): List recent execution traces, most recent first. Read from the persisted trace…, traces(), configure_observability(), Path, Observability: tracing, persistence, and the rendering of traces. Three modules…, Install the whole observability stack. Safe to call more than once. Persistence…, _details(), _label() (+10 more)

### Community 42 - "Embedding & Chunk-Size Decisions"
Cohesion: 0.12
Nodes (19): Chunk Size As The Highest-Leverage Knob, Vector Dimension Fixed In The DDL / DimensionMismatchError, Embedding Model Chosen Independently Of The Chat Model, nomic-embed-text (768 dimensions), fact_match, Container Injects Vector Width And Embedding Model Id, Lazy cached_property Container Construction, Registry And Composition Root Wiring (+11 more)

### Community 43 - "Retrieval Metrics"
Cohesion: 0.11
Nodes (18): dedupe(), hit_at_k(), mean(), percentile(), precision_at_k(), Retrieval and generation metrics. Every function here is pure: same inputs,…, Nearest-rank percentile of `values`. Nearest-rank rather than interpolated:…, Collapse repeats while preserving rank order. Retrieval returns chunks and… (+10 more)

### Community 44 - "LangChain Embedding Bridge"
Cohesion: 0.15
Nodes (11): LangChainEmbeddingModel, LangChainEmbeddingOptions, BaseModel, Vector, Catch a misconfigured `dimensions` at the first call rather than at query time.…, Adapter presenting a LangChain embeddings object as an OSC `EmbeddingModel`., _embedding_bridge(), A wrong `dimensions` would embed the corpus at one width and query at another. (+3 more)

### Community 45 - "pgvector Search & Migrations"
Cohesion: 0.17
Nodes (9): _encode_vector(), Any, Vector, Replace a document and its chunks in a single transaction. Delete-then-insert…, Apply unapplied migration files in filename order. A hand-rolled runner rather…, Fail loudly if the stored vector width disagrees with the active model.…, Render a vector in pgvector's literal form for the `::vector` cast., _to_chunk() (+1 more)

### Community 46 - "Text Extraction Parsers"
Cohesion: 0.21
Nodes (16): ParseError, A source file could not be turned into text. Raised per file and caught by the…, parse_docx(), parse_html(), parse_pdf(), parse_text(), parse_xlsx(), ParsedContent (+8 more)

### Community 47 - "Vector Store Registration"
Cohesion: 0.13
Nodes (14): The vector store could not complete an operation., VectorStoreError, Vector store providers. Imported for registration side effects., _build(), register, PostgreSQL + pgvector store: the production default. One datastore holds chunk…, Open the pool and, unless disabled, apply pending migrations., Decode JSONB into Python objects instead of raw strings. (+6 more)

### Community 48 - "Startup Banner & Composition Root"
Cohesion: 0.12
Nodes (12): Protocol, describe_startup(), Human-facing startup and shutdown reporting for the service. The structured…, Print where the service is listening and what it is running. Failures are…, _inspector(), Composition root. The only module that knows both which providers exist and how…, Close a component if it offers a way to be closed. Probed rather than required…, _release() (+4 more)

### Community 49 - "VectorStore Protocol"
Cohesion: 0.12
Nodes (8): Build the store, injecting values it cannot know on its own. Vector width, the…, Remove a document and every chunk belonging to it., Map document id to stored content hash, for incremental sync., Every document id currently indexed., Persistence and retrieval of embedded chunks. Implementations that cannot do…, Prepare the store (connect, create collections). Idempotent., The vector width this store is configured to hold., VectorStore

### Community 50 - "Persistent Tracing Design (ADR 0004)"
Cohesion: 0.23
Nodes (15): Every Case Records Its Trace Id, set_text As The Redaction Seam, Traces Are Process-Local And Lossy, trace.py — Context-Var Span Tree, HTTP Trace Endpoints Gated On development, render.py — Waterfall Renderer, store.py — Bounded Append-Only JSONL Log, One Request, One Persistent Trace (+7 more)

### Community 51 - "Observability & API Weak Points"
Cohesion: 0.14
Nodes (15): Instrument The Pipeline, Not The Adapter, A New Pipeline Stage Gets A Span, Where The Architecture Is Weakest, Operator Errors Are Messages; Bugs Are Tracebacks, Never Let A Vendor Exception Escape An Adapter, Query Rewriting (off by default), FastAPI, No Authentication, Rate Limiting Or Concurrency Bound (+7 more)

### Community 52 - "Hybrid Retrieval & RRF (ADR 0003)"
Cohesion: 0.17
Nodes (15): VectorStore Protocol, Cormack, Clarke & Buettcher, Reciprocal Rank Fusion (SIGIR 2009), Hybrid Search (default), Keyword Search (tsvector / BM25-equivalent), Reciprocal Rank Fusion (k = 60), Vector Search, ADR 0003 — Hybrid Retrieval With RRF Fused In SQL, Rejected: Fusion In Application Code Over Two Queries (+7 more)

### Community 53 - "Filesystem Loader & Corpus Boundary"
Cohesion: 0.16
Nodes (14): FilesystemLoader, Loads documents from a directory tree, one parser per format. The Phase 1…, Path, Regression: the corpus boundary is enforced by two defaults agreeing.…, test_filesystem_loader_ids_are_stable(), test_filesystem_loader_reads_a_tree(), test_missing_corpus_directory_is_an_error(), test_the_ingest_root_is_the_company_corpus_and_excludes_the_knowledge_base() (+6 more)

### Community 54 - "Memory Store Search"
Cohesion: 0.18
Nodes (9): _build(), _cosine_similarity(), _percentile(), register, Vector, In-process vector store. Not a toy: this is what makes the test suite run…, Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…, Nearest-rank percentile over a pre-sorted list. Empty input is 0. (+1 more)

### Community 55 - "Golden Set Curation & Corpus Rules"
Cohesion: 0.17
Nodes (13): Knowledge Corpus Rules — docs/company is the corpus, Measurement Rules — a retrieval change ships with a number, Abstention case set (must_abstain), expected_facts curation rule, OSC Golden Set (86 cases), OSCP Wholesale B2B FAQ corpus (17 topic files), Questions phrased as a merchant would ask them, Document-level relevance labels (+5 more)

### Community 56 - "Span Context Management"
Cohesion: 0.18
Nodes (10): ContextVar, Any, T, One stage of processing, timed. `offset_ms` is measured from the start of the…, Attach structured facts about what this stage did. Values should be small and…, Time one stage inside the active trace. Outside a trace this yields a detached…, Restore `variable`, tolerating a close in a foreign context. The streaming…, _reset() (+2 more)

### Community 57 - "Add-on Tier Pricing & Collection Slabs"
Cohesion: 0.15
Nodes (13): Add-on Tier Pricing, Cost Parameters and Profit Margins (up to 4 costs, 2 margins), Per-Variant Quantity Range Evaluation, App-Created Discount Label, Best Discount Tier Across Multiple Collections, Combined Collection Quantity Discount Slabs, OSCP Support Channel (apps@oscprofessionals.com), Offer List Drag-and-Drop Ordering (+5 more)

### Community 58 - "Experiment Profiles & Embedding Caveats"
Cohesion: 0.17
Nodes (12): Output Rules — stdout/stderr split and error hierarchy, 3072-Dimension Embedding Caveat, 384-Dimension Database Separation, BGE Asymmetric Query Prefix, cross_encoder Reranker (ms-marco-MiniLM-L-6-v2), local-only Experiment Profile, Container — composition root and lifecycle, The Five Protocol Seams (+4 more)

### Community 59 - "Chunking & Model Config Decisions"
Cohesion: 0.18
Nodes (12): Chunking settings — recursive, 900/120, Embedding choice fixes the vector width, reasoning_effort: none for Qwen3, Embeddings held local in the bridge experiment, Heading-aware markdown chunking, Local answer model misreads figures, Milestone A′ — Spend the Harness, Two scenario workbooks are 42% of the index (+4 more)

### Community 60 - "Default Profile & Retrieval Config"
Cohesion: 0.21
Nodes (12): Default profile — fully local stack, Retrieval settings — hybrid, 30 candidates, top_k 5, rrf_k 60, hosted-anthropic Experiment Profile, LangChain bridge experiment profile, Citation strength differs by provider, silently, Hybrid Retrieval, Scoped LangChain Integration, Reciprocal Rank Fusion (RRF) (+4 more)

### Community 61 - "Cart Discount & Order Limits"
Cohesion: 0.21
Nodes (12): Cart Discount, Order Limits, Row-Level Then Order-Level Discount Ordering, Row Level Discount, FEAT-04 Cart Level Discount (SCN-006, SCN-007), FEAT-05 Order Limits Min/Max (SCN-008, SCN-009), MOQ — Minimum Order Quantity (glossary), OSCP Wholesale B2B Pricing — Scenario Document (+4 more)

### Community 62 - "Offer Priority & Theme Integration"
Cohesion: 0.20
Nodes (12): Priority of the Offers, Product and Collection Page Integration, Quick Order Form, Custom Price Grid App Block / App Embed, Theme Compatibility, Tiered Pricing (collection, product and variant level), FEAT-01 Quantity Break Pricing (SCN-001, SCN-002), FEAT-07 Quick / Bulk Order Form (SCN-011) (+4 more)

### Community 63 - "Golden Set & Config Layering"
Cohesion: 0.18
Nodes (12): Abstention Cases In The Golden Set, Golden Set (86 cases), Golden-Set Path Guard Against The Index, Frozen Dataclasses For Domain Types, Layered Configuration (env > .env > YAML profile), Where Ponytail Is Deliberately Not Applied, hatchling Build Backend, The ./osc Wrapper Script (+4 more)

### Community 64 - "ChatModel Protocol"
Cohesion: 0.17
Nodes (7): A cheaper model for auxiliary steps such as query rewriting., ChatModel, StreamEvent, A text-generating model., The provider's identifier for the underlying model, for logs and traces., True if the provider resolves citations itself from structured sources. When…, Generate a response incrementally.

### Community 65 - "Retrieval Pipeline"
Cohesion: 0.21
Nodes (7): Retrieval: query rewriting, search and reranking., The retrieval pipeline: question in, ranked chunks out. rewrite -> search…, Ranked chunks plus everything needed to explain how they were selected.…, RetrievalResult, QueryRewriter, Turns a conversational turn into a standalone retrieval query., The model doing the rewriting, for traces and logs.

### Community 66 - "Trace Store"
Cohesion: 0.23
Nodes (5): Path, Record one completed trace. Never raises. A read-only filesystem, a full disk…, Completed traces, most recent first., A size-bounded, append-only log of completed traces. Two files: the one being…, TraceStore

### Community 67 - "Store Inspector"
Cohesion: 0.23
Nodes (5): Indexed documents, newest first. `search` matches title or source URI., One document's index record, or None if it is not indexed., _to_document_summary(), DocumentSummary, What the store knows about one indexed document. Distinct from `Document`: it…

### Community 68 - "Voyage Embeddings"
Cohesion: 0.23
Nodes (5): BaseModel, Vector, Adapter over the Voyage AI embeddings endpoint., VoyageEmbeddingModel, VoyageOptions

### Community 69 - "Evaluation Findings & Milestones"
Cohesion: 0.20
Nodes (11): noop reranker by default, Query rewriting off by default, Evaluation Framework, fact_match reported 1.0 for work never done, Frozen Prompts, latency_p95 of 92.9 s against a 120 s provider timeout, Measured Quality Baseline (recall@5 0.932, mrr 0.860), Milestone B — Authentication (OIDC) (+3 more)

### Community 70 - "ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split..."
Cohesion: 0.24
Nodes (11): Uniform Access Control, Directory As The Boundary, Corpus Boundary Enforced At Index Time, The Knowledge Corpus (docs/company/), workspace_id From Day One, ADR 0007 — Corpus Root Is docs/company/; The FAQ Is Split By Topic, The Corpus Root Is Named In Two Places, Rejected: An Ingest-Time Exclusion List, Provenance Edits Made During The Split (+3 more)

### Community 71 - "EmbeddedChunk"
Cohesion: 0.20
Nodes (9): Atomically replace a document and all of its chunks. Must be all-or-nothing.…, EmbeddedChunk, A chunk paired with the vector produced for it, tagged with its model. The…, embeddings(), populated(), fixture, The skip check reads a recorded hash as "chunks are present". A partial write…, Overrides the shared fixture so vectors match the target table's width. (+1 more)

### Community 72 - "OpenAICompatibleEmbeddingModel"
Cohesion: 0.29
Nodes (4): OpenAICompatibleEmbeddingModel, Vector, Release the underlying HTTP client. `Container.shutdown()` probes every…, Adapter over the `/v1/embeddings` interface.

### Community 73 - "conftest.py"
Cohesion: 0.27
Nodes (9): documents(), embeddings(), _isolate_observability(), fixture, MonkeyPatch, Path, Shared test fixtures and in-process test doubles. The doubles are deliberately…, Keep persisted traces out of the working directory, and out of each other.… (+1 more)

### Community 74 - "Path"
Cohesion: 0.20
Nodes (10): Path, A directory of .pptx looks identical to an empty corpus in the sync report., Construction alone passes with the model unpulled or the credential expired., A failing provider must be named on one line, not raised as a traceback., test_doctor_can_skip_the_live_calls(), test_doctor_makes_live_calls_by_default(), test_doctor_passes_when_every_component_is_reachable(), test_doctor_reports_a_broken_component_and_exits_non_zero() (+2 more)

### Community 75 - "Draft Order Processing"
Cohesion: 0.22
Nodes (9): Shopify Coupon Applied After Tier Discount, Draft Order Processing, 15-Minute Invoice Reuse Window, oscp-order-processing Order Tag, Server-Side Wholesale Price Validation, FEAT-10 Auto Order Tagging (SCN-014), Metafield (glossary), EC-07 Cart Discount Plus Shopify Native Discount Code (+1 more)

### Community 76 - "Chat form submit handler"
Cohesion: 0.31
Nodes (9): Complete event is authoritative, el (element factory), Grounded answer / abstention contract, Health check status banner, OSC Knowledge Assistant Web UI, Conversation history deliberately not sent, renderSources, SSE chat stream protocol (sources/delta/citation/complete/error) (+1 more)

### Community 77 - "FEAT-06 B2B Registration Form (SCN-010)"
Cohesion: 0.32
Nodes (8): CSV Export and Bulk Import of Variant Rules, Email Notification Setup (three templates), B2B Registration Form, FEAT-06 B2B Registration Form (SCN-010), FEAT-09 Bulk CSV Import/Export (SCN-013), FEAT-12 Personalised Email Notifications (SCN-016), EC-14 CSV Import Conflicts With Existing Rules, FA-09 CSV Bulk Import / Export

### Community 78 - "Four Test Tiers"
Cohesion: 0.25
Nodes (8): What Evaluation Does Not Yet Measure, Tests Never Touch The Production Corpus, Known Testing Gaps, Tests Never Write Into The Working Directory, In-Process Protocol Doubles In conftest.py, Four Test Tiers, The StubEmbeddingModel Hub Finding, pytest With asyncio_mode = auto

### Community 79 - "OSCP Wholesale B2B — Scenario Master (SCN-001..SCN-010)"
Cohesion: 0.43
Nodes (8): Acceptance Criteria Bank (AC-01..AC-19), FA-01 Tiered / Volume Pricing, FA-03 Fixed Price Rules, FA-05 B2B Registration Form, FA-06 Quick Order Form, FA-10 Manual Order Support, Merchant Archetypes Reference (MA-01..MA-07), OSCP Wholesale B2B — Scenario Master (SCN-001..SCN-010)

### Community 80 - "_HtmlTextExtractor"
Cohesion: 0.25
Nodes (4): HTMLParser, _HtmlTextExtractor, Any, Collects visible text, discarding markup and non-content elements.

### Community 81 - "GeminiEmbeddingModel"
Cohesion: 0.39
Nodes (3): GeminiEmbeddingModel, Vector, Adapter over `google-genai`'s embedding interface.

### Community 82 - "LocalEmbeddingModel"
Cohesion: 0.32
Nodes (3): LocalEmbeddingModel, Vector, Adapter over a `sentence-transformers` model loaded in-process.

### Community 83 - "CrossEncoderReranker"
Cohesion: 0.25
Nodes (4): CrossEncoderOptions, CrossEncoderReranker, BaseModel, Adapter over a `sentence-transformers` CrossEncoder.

### Community 84 - "_stub_environment()"
Cohesion: 0.25
Nodes (8): fixture, MonkeyPatch, `AssistantError` names a problem the operator must fix; frames bury it., Point the CLI at in-process doubles through configuration alone. Which is the…, The trace names the stage that raised and what every earlier stage did., _stub_environment(), test_a_failure_inside_a_stage_prints_the_trace(), test_an_operator_error_is_a_message_not_a_traceback()

### Community 85 - "FEAT-02 Customer Tag Tier Pricing (SCN-003, SCN-004)"
Cohesion: 0.33
Nodes (7): Extra Fee, Free Gift, Customer Tag (glossary), FEAT-02 Customer Tag Tier Pricing (SCN-003, SCN-004), FEAT-11 Hide Shipping Methods (SCN-015), SCN-X01 Customer-Level Fixed Price per SKU (out of scope), Customer Group Matrix (All / Logged In / Wholesale / VIP)

### Community 86 - "FEAT-03 Markets-Based Pricing (SCN-005)"
Cohesion: 0.29
Nodes (7): Market-Based Offers, Tax Display, FEAT-03 Markets-Based Pricing (SCN-005), FEAT-08 Tax Display by Country (SCN-012), Shopify Market (glossary), FA-07 Multi-Currency / Markets, FA-08 Tax Display (PDP Widget)

### Community 87 - "Operational Tooling (./osc CLI)"
Cohesion: 0.40
Nodes (6): Engineering Philosophy, Failure Diagnosis Workflow, Operational Tooling (./osc CLI), Optimisation Priority Order, OSC Engineering Handbook (AGENTS.md), CLI Command Surface (running / understanding / looking at data)

### Community 88 - "Observability Layer (trace / store / render)"
Cohesion: 0.53
Nodes (6): Observability Rules for New Code, Observability settings (buffer, span cap, persistence, capture_text), Milestone D — Deployment and Export, Observability Layer (trace / store / render), Bounded append-only JSONL trace log, Tracing is OSC's own, not OpenTelemetry and not LangChain callbacks

### Community 89 - "Session Startup Checklist"
Cohesion: 0.40
Nodes (6): Session Startup Checklist, OSC Engineering Handbook (claude.md), Knowledge-graph structural observations, OSC Internal Knowledge Assistant (Phase 4 status), OSC Knowledge Assistant (README), Server output split by audience (stderr banner, stdout JSON)

### Community 90 - "IndexStatistics"
Cohesion: 0.33
Nodes (3): Corpus-wide counts and chunk-size distribution., IndexStatistics, Aggregate state of the index. Chunk length percentiles are here because chunk…

### Community 92 - "OSCRetriever()"
Cohesion: 0.40
Nodes (5): OSCRetriever(), Any, Build a LangChain `BaseRetriever` over an OSC retrieval pipeline. A factory…, Silently spinning a second event loop would be worse than refusing., test_the_langchain_retriever_refuses_the_synchronous_path()

### Community 93 - "NoopReranker"
Cohesion: 0.40
Nodes (3): NoopReranker, Truncates the candidate list without reordering it., test_rewriting_resolves_a_follow_up_question()

### Community 94 - ".register()"
Cohesion: 0.50
Nodes (3): Factory, T, Decorator registering a factory under `name`. Re-registering a name replaces…

## Ambiguous Edges - Review These
- `Query Rewriting (off by default)` → `No Authentication, Rate Limiting Or Concurrency Bound`  [AMBIGUOUS]
  docs/engineering/architecture/retrieval.md · relation: conceptually_related_to
- `latency_p95 of 92.9 s against a 120 s provider timeout` → `Milestone B — Authentication (OIDC)`  [AMBIGUOUS]
  PROJECT_STATUS.md · relation: conceptually_related_to

## Knowledge Gaps
- **43 isolated node(s):** `osc-assistant`, `Groq + Voyage Experiment Profile`, `hosted-anthropic Experiment Profile`, `cross_encoder Reranker (ms-marco-MiniLM-L-6-v2)`, `Development PostgreSQL + pgvector Service` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Query Rewriting (off by default)` and `No Authentication, Rate Limiting Or Concurrency Bound`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `latency_p95 of 92.9 s against a 120 s provider timeout` and `Milestone B — Authentication (OIDC)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Container` connect `Container Lifecycle` to `CLI Commands — ask, ingest, search`, `HTTP API Layer`, `ChatModel Protocol`, `Evaluation CLI Command`, `Error Hierarchy & Protocol Seams`, `Ingestion Pipeline & Loaders`, `Retrieval Pipeline`, `Server Lifecycle & Startup Notes`, `Startup Banner & Composition Root`, `Settings Schema`, `VectorStore Protocol`, `LangChain Text Splitters`, `Evaluator & Answerer Composition`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `Document` connect `Ingestion Pipeline & Loaders` to `HTTP API Layer`, `Error Hierarchy & Protocol Seams`, `Faithfulness Judge & Answer Events`, `pgvector Store Interface`, `Server Lifecycle & Startup Notes`, `HTTP Layer Tests`, `Recursive Chunker`, `Settings Schema`, `Configuration Errors & Gemini Embeddings`, `LangChain Text Splitters`, `Chat Request & Response Types`, `In-Memory Vector Store`, `Markdown Chunker & LangChain Tests`, `Stub Embedding Model`, `Chunker Registration`, `Stub Chat Model & Answerer Tests`, `AssistantError Base & Loaders`, `pgvector Search & Migrations`, `Vector Store Registration`, `Startup Banner & Composition Root`, `VectorStore Protocol`, `Memory Store Search`, `ChatModel Protocol`, `Store Inspector`, `EmbeddedChunk`, `conftest.py`, `content_hash()`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `Chat Request & Response Types` to `CLI Commands — ask, ingest, search`, `ChatModel Protocol`, `Error Hierarchy & Protocol Seams`, `Stub Embedding Model`, `Faithfulness Judge & Answer Events`, `Stub Chat Model & Answerer Tests`, `Server Lifecycle & Startup Notes`, `LangChain Chat Bridge`, `Grounding & OpenAI-Compatible Chat`, `Startup Banner & Composition Root`, `VectorStore Protocol`, `Settings Schema`, `Configuration Errors & Gemini Embeddings`, `LangChain Text Splitters`, `Citation Parsing & Gemini Chat`, `Anthropic Chat Adapter`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MemoryVectorStore` (e.g. with `FailingChatModel` and `NativeCitationChatModel`) actually correct?**
  _`MemoryVectorStore` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Document` (e.g. with `ChatModel` and `Chunker`) actually correct?**
  _`Document` has 14 INFERRED edges - model-reasoned connections that need verification._