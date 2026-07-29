# Graph Report - .  (2026-07-29)

## Corpus Check
- 35 files · ~38,187 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1022 nodes · 2230 edges · 73 communities (64 shown, 9 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 195 edges (avg confidence: 0.69)
- Token cost: 177,451 input · 0 output

## Community Hubs (Navigation)
- Chunking Strategies
- Rank Fusion & Citation Grounding
- Composition Root
- In-Memory Store & Test Doubles
- Error Hierarchy
- Retrieval Settings & Tests
- Chat Request & Streaming Types
- Provider Registry
- The Five Protocol Seams
- Parser Test Suite
- pgvector Integration Tests
- HTTP Layer Tests
- API Request & Response Schemas
- Command Line Interface
- Query Rewriting & Retrieval Package
- Gemini Chat Adapter
- Reasoning-Model Output Handling
- Ingestion Idempotency & Prune Tests
- PgVectorStore Lifecycle
- HTTP Routes
- Answerer & Abstention Policy
- FastAPI App & SSE Encoding
- Anthropic Chat Adapter
- Ingestion Pipeline
- Text Extraction Parsers
- pgvector Search & Scoring
- Provider Package Registration
- Default Profile & Design Rationale
- pgvector Store Registration
- Architecture Principles & Defects
- Filesystem Loader & Tests
- Settings Schema
- Ingestion Package & Load Failures
- Embedding Provider Registration
- Engineering Handbook & Roadmap
- Storage Verification & Test Status
- Voyage Embedding Adapter
- OpenAI-Compatible Chat Adapter
- Cross-Encoder Reranker
- Embedding Width & Config Layers
- Incident Severity & Roles (corpus)
- Leave & Approval Policy (corpus)
- Deployment Runbook (corpus)
- Web UI & SSE Contract
- HTML Text Extractor
- Structured Logging
- Answer Generation Package
- Ingestion Design Decisions
- Qwen3 Context & Reasoning Config
- Memory Store & Dimension Guard
- YAML Profile Settings Source
- Reranking & Evaluation Gap
- Gemini Embedding Adapter
- Local Embedding Adapter
- OpenAI-Compatible Embeddings
- OpenAI-Compatible Presets
- Data Retention Schedule (corpus)
- Memory Store Hybrid Search
- Retrieval Pipeline
- Shared Test Fixtures
- Expense Limits & Receipts (corpus)
- PgVector Options & Fixtures
- Access Control & Records (corpus)
- Noop Reranker
- Embedding Encode Helpers
- Atomic Document Replacement
- Content Hashing
- Groq & Voyage Profile
- Package Entry Point
- StreamEvent Alias
- Registry Decorator
- Vector Type Alias

## God Nodes (most connected - your core abstractions)
1. `Document` - 48 edges
2. `ChatRequest` - 39 edges
3. `ComponentConfig` - 34 edges
4. `MemoryVectorStore` - 32 edges
5. `StubEmbeddingModel` - 32 edges
6. `ScoredChunk` - 32 edges
7. `PgVectorStore` - 31 edges
8. `StubChatModel` - 27 edges
9. `ChatModel` - 26 edges
10. `VectorStore` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Working with a Reasoning Model` --semantically_similar_to--> `4096-Token Context Budget Constraint`  [INFERRED] [semantically similar]
  README.md → PROJECT_STATUS.md
- `Grounded answer / abstention contract` --conceptually_related_to--> `Retention balance rationale`  [AMBIGUOUS]
  src/osc_assistant/api/static/index.html → docs/engineering/data-retention.pdf
- `End-of-life deletion process` --semantically_similar_to--> `Forward fix for migrations (never auto-rollback)`  [INFERRED] [semantically similar]
  docs/engineering/data-retention.pdf → docs/engineering/deployment-runbook.md
- `Retention balance rationale` --semantically_similar_to--> `Principle of least privilege`  [INFERRED] [semantically similar]
  docs/engineering/data-retention.pdf → docs/security/access-control-standard.html
- `Documentation as a First-Class Deliverable` --rationale_for--> `OSC Internal Knowledge Assistant`  [INFERRED]
  claude.md → PROJECT_STATUS.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The Five Swappable Component Seams** — project_status_chatmodel_protocol, project_status_embeddingmodel_protocol, project_status_vectorstore_protocol, project_status_reranker_protocol, project_status_chunker_protocol, project_status_registry_composition_root, project_status_domain_types_vocabulary [EXTRACTED 1.00]
- **The Citation Trust Chain (indexed text must equal source text)** — project_status_parsers_never_rewrite, project_status_chunker_corruption_defect, project_status_prompt_injection_nonce, project_status_native_vs_marker_citations, project_status_abstention_policy, project_status_local_model_misreads_figures [INFERRED 0.85]
- **Settings Deferred Until the Evaluation Harness Exists** — project_status_evaluation_harness, config_default_reranker_noop, config_default_rewrite_queries_off, config_default_chunking_budget, config_default_retrieval_hybrid, project_status_speculative_code_debt [INFERRED 0.85]
- **Streamed grounded answer flow in the web client** — src_osc_assistant_api_static_index_submithandler, src_osc_assistant_api_static_index_rendersources, src_osc_assistant_api_static_index_ssestreamprotocol, src_osc_assistant_api_static_index_completeeventauthority, src_osc_assistant_api_static_index_groundedanswercontract [EXTRACTED 1.00]
- **SEV1 incident response roles and obligations** — docs_engineering_incident_response_sev1, docs_engineering_incident_response_incidentcommander, docs_engineering_incident_response_communicationslead, docs_engineering_incident_response_scribe, docs_engineering_incident_response_communicationcadence, docs_engineering_incident_response_blamelesspostmortem [EXTRACTED 1.00]
- **Safe release control chain** — docs_engineering_deployment_runbook_predeploymentchecklist, docs_engineering_deployment_runbook_bluegreendeployment, docs_engineering_deployment_runbook_trafficshiftstages, docs_engineering_deployment_runbook_backwardcompatiblemigrations, docs_engineering_deployment_runbook_rollbackprocedure, docs_engineering_deployment_runbook_postdeploymentmonitoring [EXTRACTED 1.00]

## Communities (73 total, 9 thin omitted)

### Community 0 - "Chunking Strategies"
Cohesion: 0.08
Nodes (44): Chunking strategies. Imported for registration side effects., _build_fixed(), _build_recursive(), _chunk_id(), ChunkerOptions, FixedSizeChunker, _merge(), normalize_whitespace() (+36 more)

### Community 1 - "Rank Fusion & Citation Grounding"
Cohesion: 0.08
Nodes (40): Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…, Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…, reciprocal_rank_fusion(), _escape(), parse_marker_citations(), Grounding and citation handling for providers without native citation support.…, Escape the characters that would otherwise break out of an XML-ish attribute., Render sources as a delimited block for inclusion in a prompt. The delimiter… (+32 more)

### Community 2 - "Composition Root"
Cohesion: 0.05
Nodes (18): Self, Container, A cheaper model for auxiliary steps such as query rewriting., Builds and owns the application's components., Build the store, injecting values it cannot know on its own. Vector width, the…, Vector, Remove a document and every chunk belonging to it., Map document id to stored content hash, for incremental sync. (+10 more)

### Community 3 - "In-Memory Store & Test Doubles"
Cohesion: 0.13
Nodes (24): MemoryVectorStore, A dictionary-backed `VectorStore`., A deterministic bag-of-words embedder. Hashes each token into a fixed number of…, A chat model that returns a scripted reply. `supports_citations` is False, so…, StubChatModel, StubEmbeddingModel, _answerer(), indexed() (+16 more)

### Community 4 - "Error Hierarchy"
Cohesion: 0.10
Nodes (24): Exception, AssistantError, ConfigurationError, MissingDependencyError, ProviderError, Exception hierarchy for the assistant. A single root (`AssistantError`) lets…, Base class for every error raised by this package., The system is misconfigured and cannot start or serve a request. Raised for… (+16 more)

### Community 5 - "Retrieval Settings & Tests"
Cohesion: 0.12
Nodes (31): QueryRewriter, Reranker, EmbeddingModel, VectorStore, Tuning for the retrieval stage. Every value here is an experiment knob., RetrievalSettings, indexed(), _pipeline() (+23 more)

### Community 6 - "Chat Request & Streaming Types"
Cohesion: 0.11
Nodes (18): StreamEvent, Generate a complete response., Generate a response incrementally., ChatRequest, ChatResponse, Citation, CitationDelta, A reference from the answer back to the material that supports it. `index` is… (+10 more)

### Community 7 - "Provider Registry"
Cohesion: 0.11
Nodes (22): Factory, A component was requested by a name that is not registered., UnknownComponentError, ComponentConfig, BaseModel, A minimal registry so new providers are additions, never edits. This exists to…, Selects and configures one swappable component. `options` is intentionally…, Maps a provider name to a factory for one kind of component. (+14 more)

### Community 8 - "The Five Protocol Seams"
Cohesion: 0.12
Nodes (17): Protocol, Composition root. The only module that knows both which providers exist and how…, ChatModel, The five seams of the system. Every swappable component is defined here as a…, A second-stage relevance model applied to retrieval candidates., A text-generating model., The provider's identifier for the underlying model, for logs and traces., True if the provider resolves citations itself from structured sources. When… (+9 more)

### Community 9 - "Parser Test Suite"
Cohesion: 0.13
Nodes (24): parse(), Extract `path` using the parser registered for its extension. Raises:…, Path, Text extraction and multi-format loading tests. Two properties are load-bearing…, A page-image PDF parses cleanly and yields nothing. Indexing an empty document…, The pipeline is handed this list before iteration and reads it after, so a re-…, Provenance is denormalised onto every chunk, so it has to be right here., A corpus directory holds images and archives. They are not errors. (+16 more)

### Community 10 - "pgvector Integration Tests"
Cohesion: 0.15
Nodes (20): EmbeddedChunk, A chunk paired with the vector produced for it, tagged with its model. The…, embeddings(), populated(), fixture, StubEmbeddingModel, Integration tests for the PostgreSQL store. Skipped unless `OSC_TEST_DSN`…, Chunk ids incorporate content, so an edit yields new ids. Without the delete… (+12 more)

### Community 11 - "HTTP Layer Tests"
Cohesion: 0.14
Nodes (20): TestClient, client(), _parse_sse(), fixture, parametrize, HTTP layer tests. These run the real application — real container, real…, Validation happens at the trust boundary, before any provider is touched., Decode a server-sent event stream into (event name, payload) pairs. (+12 more)

### Community 12 - "API Request & Response Schemas"
Cohesion: 0.17
Nodes (16): AnswerBody, ChatRequestBody, CitationBody, ComponentBody, ErrorBody, HealthBody, MessageBody, BaseModel (+8 more)

### Community 13 - "Command Line Interface"
Cohesion: 0.21
Nodes (18): Argument, command, help, Option, ProfileOption, ask(), ingest(), providers() (+10 more)

### Community 14 - "Query Rewriting & Retrieval Package"
Cohesion: 0.16
Nodes (10): Retrieval: query rewriting, search and reranking., The retrieval pipeline: question in, ranked chunks out. rewrite -> search…, _format_history(), QueryRewriter, Conversational query rewriting. "What about the second one?" is not a…, Turns a conversational turn into a standalone retrieval query., Return a standalone form of `question`. With no prior turns there is nothing to…, Message (+2 more)

### Community 15 - "Gemini Chat Adapter"
Cohesion: 0.16
Nodes (12): compose_grounded_system(), Fold the system prompt, citation instruction and sources into one string. Used…, _build_contents(), _finish_reason(), GeminiChatModel, _parse_usage(), Any, StreamEvent (+4 more)

### Community 16 - "Reasoning-Model Output Handling"
Cohesion: 0.16
Nodes (17): Remove a leading `<think>` block from a reasoning model's answer. Ollama…, Fail loudly when the model produced no answer text. An empty completion…, _require_answer(), _strip_reasoning(), Reasoning-model output handling in the OpenAI-compatible adapter. Hybrid…, A block that never closes means the budget ran out mid-thought., The pattern is anchored to the start deliberately: a source document about…, The end-to-end property: markers are parsed from the stripped answer only. (+9 more)

### Community 17 - "Ingestion Idempotency & Prune Tests"
Cohesion: 0.22
Nodes (15): InMemoryLoader, Serves a fixed list of documents. Used by tests and the evaluation harness., Document, A source document as fetched by a connector, before chunking., MemoryVectorStore, Partial ingestion must not delete the rest of the corpus., Regression: a file that fails to parse is still present at the source. Pruning…, The exemption must be narrow: only the unreadable document survives. (+7 more)

### Community 18 - "PgVectorStore Lifecycle"
Cohesion: 0.13
Nodes (9): PgVectorStore, Adapter over PostgreSQL with the pgvector extension., The partition this store reads and writes. Every query is scoped to it., Apply unapplied migration files in filename order. A hand-rolled runner rather…, Fail loudly if the stored vector width disagrees with the active model.…, setup() ran the migrations; running them again must be a no-op., test_document_hashes_support_incremental_sync(), test_keyword_search_uses_the_generated_tsvector() (+1 more)

### Community 19 - "HTTP Routes"
Cohesion: 0.16
Nodes (16): AnswerBody, ChatRequestBody, get, HealthBody, post, Request, SearchRequestBody, SearchResponseBody (+8 more)

### Community 20 - "Answerer & Abstention Policy"
Cohesion: 0.21
Nodes (10): AnswerEvent, Answerer, Apply the citation policy and assemble the final answer., Answers a question against the indexed corpus., Answer `question`, returning the complete result., Answer `question`, emitting events as they become available., Ranked chunks plus everything needed to explain how they were selected., RetrievalResult (+2 more)

### Community 21 - "FastAPI App & SSE Encoding"
Cohesion: 0.18
Nodes (13): FastAPI, create_app(), FastAPI application. Thin by design: it validates input, calls one pipeline…, Build the ASGI application. Accepting settings makes the app constructible in…, Serve the bundled chat client at the site root. Registered outside the `/api`…, _register_error_handlers(), _register_ui(), encode_event() (+5 more)

### Community 22 - "Anthropic Chat Adapter"
Cohesion: 0.19
Nodes (11): AnthropicChatModel, _build_messages(), _last_user_index(), _parse_content(), _parse_usage(), Any, StreamEvent, Stream the answer, then emit citations once the message is complete. Text is… (+3 more)

### Community 23 - "Ingestion Pipeline"
Cohesion: 0.16
Nodes (11): Chunker, IngestionPipeline, EmbeddingModel, VectorStore, Delete indexed documents that the source no longer offers. `keep` is every…, Chunks, embeds and stores documents., Sync `documents` into the store. Args: documents: The full current contents of…, pipeline() (+3 more)

### Community 24 - "Text Extraction Parsers"
Cohesion: 0.23
Nodes (14): ParseError, A source file could not be turned into text. Raised per file and caught by the…, parse_docx(), parse_html(), parse_pdf(), parse_text(), ParsedContent, Path (+6 more)

### Community 25 - "pgvector Search & Scoring"
Cohesion: 0.23
Nodes (9): Return the `top_k` most relevant candidates, most relevant first., _encode_vector(), Any, Replace a document and its chunks in a single transaction. Delete-then-insert…, Render a vector in pgvector's literal form for the `::vector` cast., _to_scored_chunk(), A chunk with a relevance score. Scores are only comparable within a single…, ScoredChunk (+1 more)

### Community 26 - "Provider Package Registration"
Cohesion: 0.13
Nodes (9): Provider implementations. Importing this package registers every built-in…, AnthropicOptions, _build(), BaseModel, register, Anthropic chat provider. This is the only adapter with native citation support:…, Chat model providers. Imported for registration side effects., Reranker providers. Imported for registration side effects. (+1 more)

### Community 27 - "Default Profile & Design Rationale"
Cohesion: 0.19
Nodes (14): Documentation as a First-Class Deliverable, Default Profile (fully local), Retrieval: hybrid, 30 candidates → top 5, hosted-anthropic Experiment Profile, pgvector Image Tag Pinning Intent, Development PostgreSQL + pgvector Service, Frozen Prompts (module constants, no interpolation), Hybrid Retrieval by Default (+6 more)

### Community 28 - "pgvector Store Registration"
Cohesion: 0.15
Nodes (12): ComponentConfig, register, The vector store could not complete an operation., VectorStoreError, _build(), VectorStore, PostgreSQL + pgvector store: the production default. One datastore holds chunk…, Open the pool and, unless disabled, apply pending migrations. (+4 more)

### Community 29 - "Architecture Principles & Defects"
Cohesion: 0.19
Nodes (14): ChatModel Protocol, Chunker Content-Corruption Defect, Chunker Protocol, ComponentConfig as Architectural Hub, The Five Protocol Seams, Grounded Generation with Citations, Native Citations Where Available, Markers Elsewhere, Parsers Extract and Never Rewrite (+6 more)

### Community 30 - "Filesystem Loader & Tests"
Cohesion: 0.22
Nodes (10): _derive_title(), FilesystemLoader, Path, Use the first Markdown heading as the title, else the filename. Titles are…, Loads documents from a directory tree, one parser per format. The Phase 1…, Path, Ingestion tests. Idempotency is the property that matters: a re-run over an…, test_filesystem_loader_ids_are_stable() (+2 more)

### Community 31 - "Settings Schema"
Cohesion: 0.23
Nodes (10): OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…, ChunkingSettings, DatabaseSettings, GenerationSettings, BaseModel, Configuration. Layered, highest precedence first: process environment, then…, Root configuration object. Nested values are addressable from the environment…, ServerSettings (+2 more)

### Community 32 - "Ingestion Package & Load Failures"
Cohesion: 0.19
Nodes (9): Corpus ingestion: connectors, text extraction, and the chunk/embed/store…, Corpus connectors. A loader is any object with `load() ->…, Derive a stable id from a source URI. Hashed rather than slugified so the id is…, stable_document_id(), IngestionReport, The ingestion pipeline: documents in, embedded chunks in the store. Idempotent…, What a sync did. Returned to the CLI and logged for the admin view., LoadFailure (+1 more)

### Community 33 - "Embedding Provider Registration"
Cohesion: 0.17
Nodes (10): EmbeddingModel, A text embedding model. Document and query embedding are separate methods…, Vector width. Must match the vector store's configured dimension., _build(), register, _build(), register, _build() (+2 more)

### Community 34 - "Engineering Handbook & Roadmap"
Cohesion: 0.20
Nodes (12): Engineering Optimisation Priority Order, OSC Engineering Handbook, Session Startup Protocol, generation.max_tokens 1500, require_citations true, Abstention Is Architectural, Not a Prompt, OIDC Authentication (not implemented), OSC Internal Knowledge Assistant, Per-Document Access Control (not implemented) (+4 more)

### Community 35 - "Storage Verification & Test Status"
Cohesion: 0.23
Nodes (12): Testing Increases Confidence, Not Coverage, Default Database and Pool Settings, Shared Domain Vocabulary (types.py), Ingestion Data-Loss Defect and replace_document, Integration Suite Shares the Application Database, Generated Knowledge Graph and Its Caveats, Metadata Double-Encoding Defect (pgvector), pgvector Vector Store (+4 more)

### Community 36 - "Voyage Embedding Adapter"
Cohesion: 0.23
Nodes (5): BaseModel, Vector, Adapter over the Voyage AI embeddings endpoint., VoyageEmbeddingModel, VoyageOptions

### Community 37 - "OpenAI-Compatible Chat Adapter"
Cohesion: 0.23
Nodes (7): _make_factory(), OpenAICompatibleChatModel, _parse_usage(), Any, Adapter over the `/v1/chat/completions` interface., Stream text, resolving citations from the accumulated answer at the end.…, StreamEvent

### Community 38 - "Cross-Encoder Reranker"
Cohesion: 0.20
Nodes (7): _build(), CrossEncoderOptions, CrossEncoderReranker, BaseModel, register, Local cross-encoder reranker. A cross-encoder scores the query and candidate…, Adapter over a `sentence-transformers` CrossEncoder.

### Community 39 - "Embedding Width & Config Layers"
Cohesion: 0.25
Nodes (11): Embeddings: Ollama nomic-embed-text (768-d), 3072-Dimension Embedding Caveat, 384-Dimension Database Separation, BGE Asymmetric Query Prefix, local-only Experiment Profile, Vector Width Is Fixed at Migration Time, EmbeddingModel Protocol, Conditional HNSW Index (2000-dimension limit) (+3 more)

### Community 40 - "Incident Severity & Roles (corpus)"
Cohesion: 0.25
Nodes (11): Blameless postmortem, Incident communication cadence, Communications Lead, Incident Commander, Scribe, SEV1, SEV2, SEV3 (+3 more)

### Community 41 - "Leave & Approval Policy (corpus)"
Cohesion: 0.22
Nodes (11): Expense approval thresholds, Client entertainment rules, Rail preferred under five hours door-to-door, Flight class rules, Annual leave accrual and carryover, Leave request approval workflow, Parental leave, Public holidays (+3 more)

### Community 42 - "Deployment Runbook (corpus)"
Cohesion: 0.24
Nodes (10): Application logs (90 days hot, 12 months total), Backward-compatible database migrations, Blue-green deployment strategy, Production deployment window, Forward fix for migrations (never auto-rollback), Post-deployment monitoring and release log, Pre-deployment checklist, Rollback procedure (+2 more)

### Community 43 - "Web UI & SSE Contract"
Cohesion: 0.27
Nodes (10): Retention balance rationale, Complete event is authoritative, el (element factory), Grounded answer / abstention contract, Health check status banner, OSC Knowledge Assistant Web UI, Conversation history deliberately not sent, renderSources (+2 more)

### Community 44 - "HTML Text Extractor"
Cohesion: 0.20
Nodes (5): HTMLParser, _HtmlTextExtractor, Any, Collects visible text, discarding markup and non-content elements., The collected text, with each block element on its own line.

### Community 45 - "Structured Logging"
Cohesion: 0.22
Nodes (8): Logger, LogRecord, configure_logging(), get_logger(), JsonFormatter, Structured logging. Answers must be auditable: which chunks were retrieved,…, Renders records as single-line JSON., Install the root handler. Safe to call more than once.

### Community 46 - "Answer Generation Package"
Cohesion: 0.27
Nodes (7): AnswerComplete, Answer generation: the composition of retrieval and a chat model. This is the…, Emitted before generation so the client can render sources immediately., The authoritative final answer., RetrievalReady, Answer generation: prompts, citation policy and abstention., Prompts. These are module-level constants, never f-strings. Two reasons: 1.…

### Community 47 - "Ingestion Design Decisions"
Cohesion: 0.28
Nodes (9): Avoid Unnecessary Abstractions, Idempotent Ingestion by Content Hash, Multi-Format Document Parsing, No LLM Framework (LangChain/LlamaIndex rejected), Text Extraction Is a Plain Dict, Not a Registry, Prune Data-Loss Guard (unreadable-file exemption), Speculative Code with No Consumer, Supported Formats and Extraction (+1 more)

### Community 48 - "Qwen3 Context & Reasoning Config"
Cohesion: 0.31
Nodes (9): Chunking Sized to the 4096-Token Context (900/120), Answer Model: Ollama qwen3:8b, reasoning_effort: none (Qwen3 thinking disabled), Hosted Models Lift the Prompt Budget, 4096-Token Context Budget Constraint, One Adapter for Eight Services (openai_compatible), 'local' Provider Name Means Two Different Things, Reasoning Control Is Configuration, Not Code (+1 more)

### Community 49 - "Memory Store & Dimension Guard"
Cohesion: 0.22
Nodes (5): DimensionMismatchError, The configured embedding model does not match the store's vector width.…, _build(), register, In-process vector store. Not a toy: this is what makes the test suite run…

### Community 50 - "YAML Profile Settings Source"
Cohesion: 0.32
Nodes (5): BaseSettings, PydanticBaseSettingsSource, Any, Lowest-precedence source reading a YAML profile. The profile path comes from…, _YamlProfileSource

### Community 51 - "Reranking & Evaluation Gap"
Cohesion: 0.36
Nodes (8): fast_llm Seam (same model as the answerer), Reranker: noop (deferred until measurable), rewrite_queries: false, cross_encoder Reranker (ms-marco-MiniLM-L-6-v2), Evaluation Harness (the highest-leverage missing piece), min_score Applied Before Reranking, Query Rewriting (implemented, disabled by default), Reranker Protocol

### Community 52 - "Gemini Embedding Adapter"
Cohesion: 0.39
Nodes (3): GeminiEmbeddingModel, Vector, Adapter over `google-genai`'s embedding interface.

### Community 53 - "Local Embedding Adapter"
Cohesion: 0.32
Nodes (3): LocalEmbeddingModel, Vector, Adapter over a `sentence-transformers` model loaded in-process.

### Community 54 - "OpenAI-Compatible Embeddings"
Cohesion: 0.39
Nodes (3): OpenAICompatibleEmbeddingModel, Vector, Adapter over the `/v1/embeddings` interface.

### Community 55 - "OpenAI-Compatible Presets"
Cohesion: 0.32
Nodes (6): OpenAICompatibleOptions, _Preset, BaseModel, Chat provider for any OpenAI-compatible endpoint. One adapter covers OpenAI,…, Defaults for one OpenAI-compatible service., _resolve_key()

### Community 56 - "Data Retention Schedule (corpus)"
Cohesion: 0.43
Nodes (7): Backup snapshots (35 days), Email and instant messaging records (3 years), Customer account records (7 years), End-of-life deletion process, Legal hold, OSC Data Retention Schedule, Security audit logs (24 months, append-only)

### Community 57 - "Memory Store Hybrid Search"
Cohesion: 0.38
Nodes (4): _cosine_similarity(), Vector, Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…, _tokenize()

### Community 58 - "Retrieval Pipeline"
Cohesion: 0.47
Nodes (3): Composes rewriting, search and reranking into one call., Retrieve the chunks most relevant to `question`., RetrievalPipeline

### Community 59 - "Shared Test Fixtures"
Cohesion: 0.47
Nodes (5): documents(), embeddings(), fixture, Shared test fixtures and in-process test doubles. The doubles are deliberately…, store()

### Community 60 - "Expense Limits & Receipts (corpus)"
Cohesion: 0.40
Nodes (5): Accommodation caps, 60-day expense submission window, Daily meal allowance, Non-reimbursable expenses, Itemised receipt requirement

### Community 61 - "PgVector Options & Fixtures"
Cohesion: 0.40
Nodes (4): PgVectorOptions, BaseModel, A store scoped to a unique workspace, cleaned up afterwards. The workspace key…, store()

### Community 62 - "Access Control & Records (corpus)"
Cohesion: 0.50
Nodes (4): Recruitment records (12 or 24 months), Joiners, movers and leavers, Principle of least privilege, Service account controls

## Ambiguous Edges - Review These
- `Grounded answer / abstention contract` → `Retention balance rationale`  [AMBIGUOUS]
  src/osc_assistant/api/static/index.html · relation: conceptually_related_to
- `Staged traffic shift and automatic abort` → `Privileged production access`  [AMBIGUOUS]
  docs/engineering/deployment-runbook.md · relation: conceptually_related_to
- `Unpaid leave` → `Joiners, movers and leavers`  [AMBIGUOUS]
  docs/security/access-control-standard.html · relation: conceptually_related_to

## Knowledge Gaps
- **17 isolated node(s):** `Groq + Voyage Experiment Profile`, `osc-assistant`, `Provider Resources Are Never Released`, `fast_llm Seam (same model as the answerer)`, `Health check status banner` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Grounded answer / abstention contract` and `Retention balance rationale`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Staged traffic shift and automatic abort` and `Privileged production access`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Unpaid leave` and `Joiners, movers and leavers`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Document` connect `Ingestion Idempotency & Prune Tests` to `Chunking Strategies`, `Ingestion Package & Load Failures`, `Embedding Provider Registration`, `Composition Root`, `Atomic Document Replacement`, `Content Hashing`, `Chat Request & Streaming Types`, `In-Memory Store & Test Doubles`, `The Five Protocol Seams`, `Retrieval Settings & Tests`, `pgvector Integration Tests`, `HTTP Layer Tests`, `Memory Store & Dimension Guard`, `Ingestion Pipeline`, `pgvector Search & Scoring`, `Shared Test Fixtures`, `pgvector Store Registration`, `Filesystem Loader & Tests`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `Chat Request & Streaming Types` to `Chunking Strategies`, `Rank Fusion & Citation Grounding`, `Embedding Provider Registration`, `Composition Root`, `In-Memory Store & Test Doubles`, `OpenAI-Compatible Chat Adapter`, `The Five Protocol Seams`, `Answer Generation Package`, `Gemini Chat Adapter`, `Query Rewriting & Retrieval Package`, `Answerer & Abstention Policy`, `Anthropic Chat Adapter`, `OpenAI-Compatible Presets`, `Provider Package Registration`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `ProviderError` connect `Error Hierarchy` to `Embedding Provider Registration`, `Voyage Embedding Adapter`, `OpenAI-Compatible Chat Adapter`, `The Five Protocol Seams`, `Gemini Chat Adapter`, `Reasoning-Model Output Handling`, `Gemini Embedding Adapter`, `OpenAI-Compatible Presets`, `OpenAI-Compatible Embeddings`, `Anthropic Chat Adapter`, `Provider Package Registration`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `Document` (e.g. with `ChatModel` and `Chunker`) actually correct?**
  _`Document` has 9 INFERRED edges - model-reasoned connections that need verification._