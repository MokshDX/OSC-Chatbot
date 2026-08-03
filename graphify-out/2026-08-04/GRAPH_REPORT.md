# Graph Report - .  (2026-08-04)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1624 nodes · 3841 edges · 104 communities (84 shown, 20 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 372 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3eb9a8b6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ChunkerOptions
- test_fusion_and_grounding.py
- VectorStore
- StubEmbeddingModel
- MissingDependencyError
- test_retrieval.py
- ChatRequest
- Registry
- ChatModel
- test_parsers.py
- PgVectorStore
- test_api.py
- schemas.py
- trace
- container.py
- ProviderError
- grounding.py
- Document
- ._migrate
- chat
- answerer.py
- app.py
- anthropic_provider.py
- .ingest
- parsers.py
- ._acquire
- memory.py
- Default Profile (fully local)
- .setup
- The Five Protocol Seams
- ingestion/__init__.py
- test_server_lifecycle.py
- Chunk
- ComponentConfig
- OSC Internal Knowledge Assistant
- pgvector Vector Store
- VoyageEmbeddingModel
- llm/openai_compatible.py
- Reranker
- local-only Experiment Profile
- SEV1
- Annual leave accrual and carryover
- Rollback procedure
- Chat form submit handler
- _HtmlTextExtractor
- trace.py
- Container
- Avoid Unnecessary Abstractions
- 4096-Token Context Budget Constraint
- errors.py
- load_settings
- Evaluation Harness (the highest-leverage missing piece)
- GeminiEmbeddingModel
- LocalEmbeddingModel
- OpenAICompatibleEmbeddingModel
- llm/langchain_bridge.py
- OSC Data Retention Schedule
- .search_hybrid
- ScoredChunk
- conftest.py
- Itemised receipt requirement
- PgVectorOptions
- Principle of least privilege
- core.py
- ._encode
- MemoryVectorStore
- content_hash
- Groq + Voyage Experiment Profile
- osc-assistant
- recursive.py
- load
- Span
- diagnose.py
- test_cli.py
- test_e2e.py
- test_langchain_integration.py
- AGENTS.md
- Trace
- TraceStore
- _FakeEmbeddings
- providers/__init__.py
- LangChainChunkerOptions
- _document
- Path
- LangChainEmbeddingModel
- _stub_environment
- populated
- .split
- .shutdown
- 001_init.sql
- osc
- integrations/__init__.py
- .dimensions
- _make_factory
- .workspace_id
- test_config_redacts_credentials_by_default
- test_ask_explain_prints_the_execution_trace
- test_traces_are_readable_after_the_command_that_made_them_exited
- test_trace_with_no_id_expands_the_most_recent
- test_traces_can_be_filtered_by_name
- test_trace_reports_an_unreachable_service_actionably
- test_help_groups_commands_by_purpose
- pipeline

## God Nodes (most connected - your core abstractions)
1. `MemoryVectorStore` - 71 edges
2. `Document` - 68 edges
3. `StubEmbeddingModel` - 67 edges
4. `ComponentConfig` - 64 edges
5. `Container` - 57 edges
6. `ChatRequest` - 57 edges
7. `PgVectorStore` - 43 edges
8. `StubChatModel` - 39 edges
9. `ScoredChunk` - 36 edges
10. `trace()` - 33 edges

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

## Communities (104 total, 20 thin omitted)

### Community 0 - "ChunkerOptions"
Cohesion: 0.14
Nodes (27): ChunkerOptions, BaseModel, Splits on the coarsest separator that keeps chunks under the target size. Falls…, RecursiveChunker, _document(), Chunking tests. Chunk id stability is the load-bearing property here: ingestion…, Chunk text is quoted back to users as citation evidence, so the chunker must…, Ingestion skips unchanged documents by hash; ids must not drift. (+19 more)

### Community 1 - "test_fusion_and_grounding.py"
Cohesion: 0.11
Nodes (33): Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…, reciprocal_rank_fusion(), parse_marker_citations(), Render sources as a delimited block for inclusion in a prompt. The delimiter…, Extract citations from `[n]` markers in `text`. Markers referring to a source…, render_sources(), _chunk(), _ranking() (+25 more)

### Community 2 - "VectorStore"
Cohesion: 0.11
Nodes (11): Build the store, injecting values it cannot know on its own. Vector width, the…, Remove a document and every chunk belonging to it., Map document id to stored content hash, for incremental sync., Every document id currently indexed., Persistence and retrieval of embedded chunks. Implementations that cannot do…, Prepare the store (connect, create collections). Idempotent., The vector width this store is configured to hold., VectorStore (+3 more)

### Community 3 - "StubEmbeddingModel"
Cohesion: 0.17
Nodes (20): A deterministic bag-of-words embedder. Hashes each token into a fixed number of…, A chat model that returns a scripted reply. `supports_citations` is False, so…, StubChatModel, StubEmbeddingModel, _answerer(), Answer generation tests. The abstention policy is the system's main defence…, Both citation paths must produce the same shape for downstream code., The complete event is authoritative: clients discard streamed text when it… (+12 more)

### Community 4 - "MissingDependencyError"
Cohesion: 0.14
Nodes (14): ConfigurationError, MissingDependencyError, The system is misconfigured and cannot start or serve a request. Raised for…, A provider was selected but its optional dependency is not installed., GeminiEmbeddingOptions, BaseModel, _instantiate(), Any (+6 more)

### Community 5 - "test_retrieval.py"
Cohesion: 0.12
Nodes (21): NoopReranker, Truncates the candidate list without reordering it., Tuning for the retrieval stage. Every value here is an experiment knob., RetrievalSettings, _pipeline(), parametrize, Retrieval tests, including the vector store contract. `test_store_contract`…, Regression: the threshold must not be measured against reranker output. A… (+13 more)

### Community 6 - "ChatRequest"
Cohesion: 0.11
Nodes (19): StreamEvent, Generate a response incrementally., StreamEvent, Stream text, resolving citations from the accumulated answer at the end.…, ChatRequest, Citation, CitationDelta, A reference from the answer back to the material that supports it. `index` is… (+11 more)

### Community 7 - "Registry"
Cohesion: 0.12
Nodes (16): Factory, T, Maps a provider name to a factory for one kind of component., Decorator registering a factory under `name`. Re-registering a name replaces…, Registry, parametrize, The registry is the mechanism that makes providers pluggable, so it is tested…, Overriding a built-in must be possible without editing it. (+8 more)

### Community 8 - "ChatModel"
Cohesion: 0.14
Nodes (10): ChatModel, A text-generating model., The provider's identifier for the underlying model, for logs and traces., True if the provider resolves citations itself from structured sources. When…, Generate a complete response., _build(), register, _build() (+2 more)

### Community 9 - "test_parsers.py"
Cohesion: 0.13
Nodes (24): parse(), Extract `path` using the parser registered for its extension. Raises:…, Path, Text extraction and multi-format loading tests. Two properties are load-bearing…, A page-image PDF parses cleanly and yields nothing. Indexing an empty document…, The pipeline is handed this list before iteration and reads it after, so a re-…, Provenance is denormalised onto every chunk, so it has to be right here., A corpus directory holds images and archives. They are not errors. (+16 more)

### Community 10 - "PgVectorStore"
Cohesion: 0.12
Nodes (22): PgVectorStore, Adapter over PostgreSQL with the pgvector extension., Integration tests for the PostgreSQL store. Skipped unless `OSC_TEST_DSN`…, setup() ran the migrations; running them again must be a no-op., Chunk ids incorporate content, so an edit yields new ids. Without the delete…, The skip check reads a recorded hash as "chunks are present". A partial write…, A correlated subquery, not a join: this document is the one worth finding. It…, test_a_chunk_round_trips_with_its_metadata() (+14 more)

### Community 11 - "test_api.py"
Cohesion: 0.10
Nodes (32): client(), _development_client(), _parse_sse(), fixture, parametrize, TestClient, HTTP layer tests. These run the real application — real container, real…, Validation happens at the trust boundary, before any provider is touched. (+24 more)

### Community 12 - "schemas.py"
Cohesion: 0.14
Nodes (19): AnswerBody, ChatRequestBody, CitationBody, ComponentBody, ErrorBody, HealthBody, MessageBody, Any (+11 more)

### Community 13 - "trace"
Cohesion: 0.06
Nodes (59): Expand one execution trace into a stage-by-stage waterfall. With no id this…, trace(), active_trace_store(), The store traces are being written to, if persistence is enabled., configure_tracing(), Process-wide tracing behaviour, set once from settings at startup. Module-level…, Install tracing configuration. Safe to call more than once., TraceConfig (+51 more)

### Community 14 - "container.py"
Cohesion: 0.14
Nodes (14): Composition root. The only module that knows both which providers exist and how…, OSCRetriever(), Any, Build a LangChain `BaseRetriever` over an OSC retrieval pipeline. A factory…, Retrieval: query rewriting, search and reranking., The retrieval pipeline: question in, ranked chunks out. rewrite -> search…, Composes rewriting, search and reranking into one call., RetrievalPipeline (+6 more)

### Community 15 - "ProviderError"
Cohesion: 0.19
Nodes (12): ProviderError, An upstream provider (LLM, embeddings, reranker) failed., _build_contents(), _finish_reason(), GeminiChatModel, _parse_usage(), Any, StreamEvent (+4 more)

### Community 16 - "grounding.py"
Cohesion: 0.13
Nodes (20): _escape(), Grounding and citation handling for providers without native citation support.…, Remove a leading `<think>` block from a reasoning model's answer. Ollama…, Fail loudly when the model produced no answer text. An empty completion…, Escape the characters that would otherwise break out of an XML-ish attribute., require_answer(), strip_reasoning(), Reasoning-model output handling in the OpenAI-compatible adapter. Hybrid… (+12 more)

### Community 17 - "Document"
Cohesion: 0.13
Nodes (29): InMemoryLoader, Serves a fixed list of documents. Used by tests and the evaluation harness., IngestionPipeline, Chunks, embeds and stores documents., Document, A source document as fetched by a connector, before chunking., indexed(), fixture (+21 more)

### Community 19 - "chat"
Cohesion: 0.13
Nodes (21): get, post, Request, chat(), _container(), get_trace(), health(), list_traces() (+13 more)

### Community 20 - "answerer.py"
Cohesion: 0.06
Nodes (38): AnswerEvent, _answer_payload(), _print_answer(), _annotate_abstention(), _annotate_generation(), AnswerComplete, Answerer, Answer generation: the composition of retrieval and a chat model. This is the… (+30 more)

### Community 21 - "app.py"
Cohesion: 0.15
Nodes (19): FastAPI, create_app(), FastAPI application. Thin by design: it validates input, calls one pipeline…, Serve the bundled chat client at the site root. Registered outside the `/api`…, Build the ASGI application. Accepting settings makes the app constructible in…, _register_error_handlers(), _register_ui(), describe_shutdown() (+11 more)

### Community 22 - "anthropic_provider.py"
Cohesion: 0.15
Nodes (16): AnthropicChatModel, AnthropicOptions, _build_messages(), _last_user_index(), _parse_content(), _parse_usage(), Any, BaseModel (+8 more)

### Community 23 - ".ingest"
Cohesion: 0.25
Nodes (5): Chunk, embed and store one document. Each of the three stages gets its own…, Delete indexed documents that the source no longer offers. `keep` is every…, Sync `documents` into the store. Args: documents: The full current contents of…, LoadFailure, A source file a connector found but could not turn into a `Document`. Carries…

### Community 24 - "parsers.py"
Cohesion: 0.23
Nodes (14): ParseError, A source file could not be turned into text. Raised per file and caught by the…, parse_docx(), parse_html(), parse_pdf(), parse_text(), ParsedContent, Path (+6 more)

### Community 25 - "._acquire"
Cohesion: 0.18
Nodes (7): LogRecord, _encode_vector(), Vector, Replace a document and its chunks in a single transaction. Delete-then-insert…, Render a vector in pgvector's literal form for the `::vector` cast., _to_chunk(), _to_scored_chunk()

### Community 26 - "memory.py"
Cohesion: 0.13
Nodes (13): Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…, Corpus-wide counts and chunk-size distribution., _build(), _percentile(), register, In-process vector store. Not a toy: this is what makes the test suite run…, Nearest-rank percentile over a pre-sorted list. Empty input is 0., IndexStatistics (+5 more)

### Community 27 - "Default Profile (fully local)"
Cohesion: 0.19
Nodes (13): Documentation as a First-Class Deliverable, Default Database and Pool Settings, Default Profile (fully local), hosted-anthropic Experiment Profile, pgvector Image Tag Pinning Intent, Development PostgreSQL + pgvector Service, Frozen Prompts (module constants, no interpolation), Integration Suite Shares the Application Database (+5 more)

### Community 28 - ".setup"
Cohesion: 0.20
Nodes (7): Any, Open the pool and, unless disabled, apply pending migrations., Decode JSONB into Python objects instead of raw strings., Strip the password from a DSN before it reaches a terminal or a log. Connection…, _redact_dsn(), _register_codecs(), _to_document_summary()

### Community 29 - "The Five Protocol Seams"
Cohesion: 0.19
Nodes (14): ChatModel Protocol, Chunker Content-Corruption Defect, Chunker Protocol, ComponentConfig as Architectural Hub, The Five Protocol Seams, Grounded Generation with Citations, Native Citations Where Available, Markers Elsewhere, Parsers Extract and Never Rewrite (+6 more)

### Community 30 - "ingestion/__init__.py"
Cohesion: 0.14
Nodes (15): Corpus ingestion: connectors, text extraction, and the chunk/embed/store…, _derive_title(), FilesystemLoader, Path, Corpus connectors. A loader is any object with `load() ->…, Use the first Markdown heading as the title, else the filename. Titles are…, Derive a stable id from a source URI. Hashed rather than slugified so the id is…, Loads documents from a directory tree, one parser per format. The Phase 1… (+7 more)

### Community 31 - "test_server_lifecycle.py"
Cohesion: 0.06
Nodes (47): ChunkingSettings, DatabaseSettings, GenerationSettings, ObservabilitySettings, BaseModel, Configuration. Layered, highest precedence first: process environment, then…, How much the system records about its own execution. Defaults are chosen for a…, ServerSettings (+39 more)

### Community 32 - "Chunk"
Cohesion: 0.09
Nodes (20): Protocol, The ingestion pipeline: documents in, embedded chunks in the store. Idempotent…, Chunker, Read-only introspection of what a store currently holds. Kept **separate from…, Indexed documents, newest first. `search` matches title or source URI., One document's index record, or None if it is not indexed., Every chunk of a document, in ordinal order., One chunk with its full text — what the model was actually shown. (+12 more)

### Community 33 - "ComponentConfig"
Cohesion: 0.11
Nodes (29): _build_langchain_recursive(), _build_markdown(), register, Chunkers backed by `langchain-text-splitters`. **Why adopt a library here, of…, EmbeddingModel, The five seams of the system. Every swappable component is defined here as a…, A text embedding model. Document and query embedding are separate methods…, _build() (+21 more)

### Community 34 - "OSC Internal Knowledge Assistant"
Cohesion: 0.18
Nodes (13): Engineering Optimisation Priority Order, OSC Engineering Handbook, Session Startup Protocol, generation.max_tokens 1500, require_citations true, Abstention Is Architectural, Not a Prompt, Generated Knowledge Graph and Its Caveats, OIDC Authentication (not implemented), OSC Internal Knowledge Assistant (+5 more)

### Community 35 - "pgvector Vector Store"
Cohesion: 0.23
Nodes (12): Testing Increases Confidence, Not Coverage, Retrieval: hybrid, 30 candidates → top 5, Shared Domain Vocabulary (types.py), Hybrid Retrieval by Default, Ingestion Data-Loss Defect and replace_document, Metadata Double-Encoding Defect (pgvector), One Datastore (PostgreSQL holds everything), pgvector Vector Store (+4 more)

### Community 36 - "VoyageEmbeddingModel"
Cohesion: 0.23
Nodes (5): BaseModel, Vector, Adapter over the Voyage AI embeddings endpoint., VoyageEmbeddingModel, VoyageOptions

### Community 37 - "llm/openai_compatible.py"
Cohesion: 0.15
Nodes (12): compose_grounded_system(), Fold the system prompt, citation instruction and sources into one string. Used…, Chat model providers. Imported for registration side effects., _make_factory(), OpenAICompatibleChatModel, _parse_usage(), _Preset, Any (+4 more)

### Community 38 - "Reranker"
Cohesion: 0.12
Nodes (11): A second-stage relevance model applied to retrieval candidates., Return the `top_k` most relevant candidates, most relevant first., Reranker, _build(), CrossEncoderOptions, CrossEncoderReranker, BaseModel, register (+3 more)

### Community 39 - "local-only Experiment Profile"
Cohesion: 0.25
Nodes (11): Embeddings: Ollama nomic-embed-text (768-d), 3072-Dimension Embedding Caveat, 384-Dimension Database Separation, BGE Asymmetric Query Prefix, local-only Experiment Profile, Vector Width Is Fixed at Migration Time, EmbeddingModel Protocol, Conditional HNSW Index (2000-dimension limit) (+3 more)

### Community 40 - "SEV1"
Cohesion: 0.25
Nodes (11): Blameless postmortem, Incident communication cadence, Communications Lead, Incident Commander, Scribe, SEV1, SEV2, SEV3 (+3 more)

### Community 41 - "Annual leave accrual and carryover"
Cohesion: 0.22
Nodes (11): Expense approval thresholds, Client entertainment rules, Rail preferred under five hours door-to-door, Flight class rules, Annual leave accrual and carryover, Leave request approval workflow, Parental leave, Public holidays (+3 more)

### Community 42 - "Rollback procedure"
Cohesion: 0.24
Nodes (10): Application logs (90 days hot, 12 months total), Backward-compatible database migrations, Blue-green deployment strategy, Production deployment window, Forward fix for migrations (never auto-rollback), Post-deployment monitoring and release log, Pre-deployment checklist, Rollback procedure (+2 more)

### Community 43 - "Chat form submit handler"
Cohesion: 0.27
Nodes (10): Retention balance rationale, Complete event is authoritative, el (element factory), Grounded answer / abstention contract, Health check status banner, OSC Knowledge Assistant Web UI, Conversation history deliberately not sent, renderSources (+2 more)

### Community 44 - "_HtmlTextExtractor"
Cohesion: 0.20
Nodes (5): HTMLParser, _HtmlTextExtractor, Any, Collects visible text, discarding markup and non-content elements., The collected text, with each block element on its own line.

### Community 45 - "trace.py"
Cohesion: 0.13
Nodes (18): Logger, get_logger(), JsonFormatter, Structured logging. Answers must be auditable: which chunks were retrieved,…, Renders records as single-line JSON., configure_observability(), Path, Observability: tracing, persistence, and the rendering of traces. Three modules… (+10 more)

### Community 46 - "Container"
Cohesion: 0.12
Nodes (19): Self, Check, _check_chunker(), _check_corpus(), _check_langchain(), _check_llm(), _check_reranker(), _check_store() (+11 more)

### Community 47 - "Avoid Unnecessary Abstractions"
Cohesion: 0.28
Nodes (9): Avoid Unnecessary Abstractions, Idempotent Ingestion by Content Hash, Multi-Format Document Parsing, No LLM Framework (LangChain/LlamaIndex rejected), Text Extraction Is a Plain Dict, Not a Registry, Prune Data-Loss Guard (unreadable-file exemption), Speculative Code with No Consumer, Supported Formats and Extraction (+1 more)

### Community 48 - "4096-Token Context Budget Constraint"
Cohesion: 0.31
Nodes (9): Chunking Sized to the 4096-Token Context (900/120), Answer Model: Ollama qwen3:8b, reasoning_effort: none (Qwen3 thinking disabled), Hosted Models Lift the Prompt Budget, 4096-Token Context Budget Constraint, One Adapter for Eight Services (openai_compatible), 'local' Provider Name Means Two Different Things, Reasoning Control Is Configuration, Not Code (+1 more)

### Community 49 - "errors.py"
Cohesion: 0.16
Nodes (10): Exception, AssistantError, DimensionMismatchError, Exception hierarchy for the assistant. A single root (`AssistantError`) lets…, Base class for every error raised by this package., A component was requested by a name that is not registered., The vector store could not complete an operation., The configured embedding model does not match the store's vector width.… (+2 more)

### Community 50 - "load_settings"
Cohesion: 0.10
Nodes (30): BaseSettings, PydanticBaseSettingsSource, load_settings(), Any, Lowest-precedence source reading a YAML profile. The profile path comes from…, Build settings, applying `overrides` at the highest precedence., _YamlProfileSource, _isolate_environment() (+22 more)

### Community 51 - "Evaluation Harness (the highest-leverage missing piece)"
Cohesion: 0.36
Nodes (8): fast_llm Seam (same model as the answerer), Reranker: noop (deferred until measurable), rewrite_queries: false, cross_encoder Reranker (ms-marco-MiniLM-L-6-v2), Evaluation Harness (the highest-leverage missing piece), min_score Applied Before Reranking, Query Rewriting (implemented, disabled by default), Reranker Protocol

### Community 52 - "GeminiEmbeddingModel"
Cohesion: 0.39
Nodes (3): GeminiEmbeddingModel, Vector, Adapter over `google-genai`'s embedding interface.

### Community 53 - "LocalEmbeddingModel"
Cohesion: 0.22
Nodes (5): LocalEmbeddingModel, LocalEmbeddingOptions, BaseModel, Vector, Adapter over a `sentence-transformers` model loaded in-process.

### Community 54 - "OpenAICompatibleEmbeddingModel"
Cohesion: 0.39
Nodes (3): OpenAICompatibleEmbeddingModel, Vector, Adapter over the `/v1/embeddings` interface.

### Community 55 - "llm/langchain_bridge.py"
Cohesion: 0.13
Nodes (20): _build(), _instantiate(), LangChainChatModel, _parse_usage(), Any, register, StreamEvent, Chat provider backed by any LangChain `BaseChatModel`. **Why this exists.** OSC… (+12 more)

### Community 56 - "OSC Data Retention Schedule"
Cohesion: 0.43
Nodes (7): Backup snapshots (35 days), Email and instant messaging records (3 years), Customer account records (7 years), End-of-life deletion process, Legal hold, OSC Data Retention Schedule, Security audit logs (24 months, append-only)

### Community 57 - ".search_hybrid"
Cohesion: 0.38
Nodes (4): _cosine_similarity(), Vector, Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…, _tokenize()

### Community 58 - "ScoredChunk"
Cohesion: 0.12
Nodes (12): LangChainDocument, Exposing OSC to LangChain, rather than the other way round. Every other…, Translate one retrieval hit into a LangChain document. The score and the match…, to_langchain_document(), Vector, Lexical search. Return `[]` if the store has no lexical index., Combined lexical and vector search, fused into a single ranking., Embed corpus text. Returns one vector per input, in order. (+4 more)

### Community 59 - "conftest.py"
Cohesion: 0.27
Nodes (9): documents(), embeddings(), _isolate_observability(), fixture, MonkeyPatch, Path, Shared test fixtures and in-process test doubles. The doubles are deliberately…, Keep persisted traces out of the working directory, and out of each other.… (+1 more)

### Community 60 - "Itemised receipt requirement"
Cohesion: 0.40
Nodes (5): Accommodation caps, 60-day expense submission window, Daily meal allowance, Non-reimbursable expenses, Itemised receipt requirement

### Community 61 - "PgVectorOptions"
Cohesion: 0.22
Nodes (8): PgVectorOptions, BaseModel, Content in one workspace must be invisible to another., Vectors from a different model must never be compared against these., Every aggregate carries the partition key, or a shared database lies., test_search_ignores_other_embedding_models(), test_statistics_are_scoped_to_the_workspace(), test_workspace_isolates_queries()

### Community 62 - "Principle of least privilege"
Cohesion: 0.50
Nodes (4): Recruitment records (12 or 24 months), Joiners, movers and leavers, Principle of least privilege, Service account controls

### Community 63 - "core.py"
Cohesion: 0.15
Nodes (25): ExplainOption, ask(), ingest(), _print_trace(), Argument, command, help, JsonOption (+17 more)

### Community 65 - "MemoryVectorStore"
Cohesion: 0.09
Nodes (17): MemoryVectorStore, A dictionary-backed `VectorStore`., Replace a document and its chunks. Atomic by construction: the vectors are…, Store inspection tests. `StoreInspector` is what the operational commands are…, The last step of verifying a citation: the exact text the model was shown., The protocol is optional; a store that cannot support it is still a store. Both…, The point of measuring is comparing against the configured target. A…, test_a_chunk_can_be_fetched_by_id() (+9 more)

### Community 69 - "recursive.py"
Cohesion: 0.11
Nodes (20): Chunking strategies. Imported for registration side effects., LangChainRecursiveChunker, `RecursiveCharacterTextSplitter` behind the OSC `Chunker` protocol., _build_fixed(), _build_recursive(), _chunk_id(), FixedSizeChunker, _merge() (+12 more)

### Community 70 - "load"
Cohesion: 0.16
Nodes (26): chunk(), config(), doctor(), document(), documents(), providers(), Argument, command (+18 more)

### Community 71 - "Span"
Cohesion: 0.10
Nodes (20): ContextVar, _details(), _label(), Rendering a trace for a human. Separate from `trace` because collection and…, Draw the trace as an indented waterfall. Bars are positioned by `offset_ms` and…, The first few attributes, plus any error. Truncated on purpose: a waterfall is…, render_waterfall(), _short() (+12 more)

### Community 73 - "diagnose.py"
Cohesion: 0.13
Nodes (19): _document_payload(), _fetch_traces(), _inspector(), Any, Diagnostics and inspection: understanding the system without reading its…, Blank anything whose key suggests a credential. Name-based rather than value-…, List recent execution traces, most recent first. Read from the persisted trace…, _redact() (+11 more)

### Community 75 - "test_e2e.py"
Cohesion: 0.11
Nodes (18): End-to-end smoke test against the real stack. Everything else in this suite…, The property that makes a scheduled sync cheap and safe to re-run., Real embeddings, real pgvector, real SQL rank fusion., The whole path, against a real model. Asserts grounding, not wording.…, General knowledge must not leak in where the corpus is silent., Proves extraction, not just ingestion: a PDF whose text never parsed would…, The abstention policy must be identical in both modes., Every stage of the real pipeline, timed — the observability contract itself. (+10 more)

### Community 76 - "test_langchain_integration.py"
Cohesion: 0.16
Nodes (16): LangChainChatOptions, BaseModel, _bridge(), LangChain integration tests. Three surfaces, three concerns: * **Chunkers** —…, A bridge over LangChain's own fake chat model — no network, no credential., The streaming contract must match the OpenAI-compatible adapter's exactly., An empty answer looks identical to "the corpus has nothing" further down., A `[2]` written while thinking aloud must never become a citation. (+8 more)

### Community 77 - "AGENTS.md"
Cohesion: 0.12
Nodes (15): Architecture & Code Standards, Comments, Documentation & Testing, Communication, Current Project, Definition of Success, Dependencies & Repository Rules, Diagnosing a failure, Engineering Philosophy (+7 more)

### Community 78 - "Trace"
Cohesion: 0.14
Nodes (8): _log_trace(), Everything one operation did, as a flat list of spans in start order. Flat…, The leaf span that consumed the most wall time. Leaves only: a parent's…, A bounded ring of recent traces, for `osc-assistant trace` and `/api/traces`.…, Begin a root trace for one operation (a request, a CLI command, a sync).…, Emit the whole trace as one structured record. One line per operation rather…, Trace, TraceRecorder

### Community 79 - "TraceStore"
Cohesion: 0.17
Nodes (7): Path, Record one completed trace. Never raises. A read-only filesystem, a full disk…, Completed traces, most recent first., Look up by full id, or by a unique prefix — ids get pasted by hand., Yield traces newest first, current file before rotated. Reads whole files…, A size-bounded, append-only log of completed traces. Two files: the one being…, TraceStore

### Community 80 - "_FakeEmbeddings"
Cohesion: 0.23
Nodes (10): Embeddings, LangChainEmbeddingOptions, BaseModel, _embedding_bridge(), _FakeEmbeddings, A LangChain `Embeddings` with no dependencies. LangChain's own…, A wrong `dimensions` would embed the corpus at one width and query at another., test_embedding_bridge_rejects_a_misdeclared_width() (+2 more)

### Community 81 - "providers/__init__.py"
Cohesion: 0.33
Nodes (3): Provider implementations. Importing this package registers every built-in…, Reranker providers. Imported for registration side effects., Vector store providers. Imported for registration side effects.

### Community 82 - "LangChainChunkerOptions"
Cohesion: 0.23
Nodes (10): LangChainChunkerOptions, MarkdownChunker, Heading-aware splitting: structure first, then size. Two passes, because either…, `ChunkerOptions` plus the settings only the LangChain splitters expose., _require_splitters(), A retrieval hit should say which section it came from without a second lookup., Stripping the heading would make the stored text differ from the source., test_empty_document_produces_no_chunks() (+2 more)

### Community 83 - "_document"
Cohesion: 0.21
Nodes (12): _document(), parametrize, Chunk text is quoted back as citation evidence, so no character may be…, The reason for adopting the library: OSC's own chunker can overshoot by the…, No separator exists in one long token; the hard fallback must catch it., Ingestion skips unchanged documents by hash; drifting ids would re-index all., test_chunk_ids_are_stable_across_runs(), test_chunking_preserves_document_content() (+4 more)

### Community 84 - "Path"
Cohesion: 0.20
Nodes (10): Path, A directory of .pptx looks identical to an empty corpus in the sync report., Construction alone passes with the model unpulled or the credential expired., A failing provider must be named on one line, not raised as a traceback., test_doctor_can_skip_the_live_calls(), test_doctor_makes_live_calls_by_default(), test_doctor_passes_when_every_component_is_reachable(), test_doctor_reports_a_broken_component_and_exits_non_zero() (+2 more)

### Community 85 - "LangChainEmbeddingModel"
Cohesion: 0.31
Nodes (4): LangChainEmbeddingModel, Vector, Catch a misconfigured `dimensions` at the first call rather than at query time.…, Adapter presenting a LangChain embeddings object as an OSC `EmbeddingModel`.

### Community 86 - "_stub_environment"
Cohesion: 0.25
Nodes (8): fixture, MonkeyPatch, `AssistantError` names a problem the operator must fix; frames bury it., Point the CLI at in-process doubles through configuration alone. Which is the…, The trace names the stage that raised and what every earlier stage did., _stub_environment(), test_a_failure_inside_a_stage_prints_the_trace(), test_an_operator_error_is_a_message_not_a_traceback()

### Community 87 - "populated"
Cohesion: 0.33
Nodes (6): embeddings(), populated(), fixture, Overrides the shared fixture so vectors match the target table's width., A store scoped to a unique workspace, cleaned up afterwards. The workspace key…, store()

### Community 88 - ".split"
Cohesion: 0.50
Nodes (4): _heading_path(), Any, Join whichever heading levels are present into a readable path., _section_metadata()

### Community 89 - ".shutdown"
Cohesion: 0.40
Nodes (3): Release everything that was actually built. Only components whose…, Close a component if it offers a way to be closed. Probed rather than required…, _release()

## Ambiguous Edges - Review These
- `Grounded answer / abstention contract` → `Retention balance rationale`  [AMBIGUOUS]
  src/osc_assistant/api/static/index.html · relation: conceptually_related_to
- `Staged traffic shift and automatic abort` → `Privileged production access`  [AMBIGUOUS]
  docs/engineering/deployment-runbook.md · relation: conceptually_related_to
- `Unpaid leave` → `Joiners, movers and leavers`  [AMBIGUOUS]
  docs/security/access-control-standard.html · relation: conceptually_related_to

## Knowledge Gaps
- **30 isolated node(s):** `osc-assistant`, `Purpose`, `Current Project`, `Engineering Philosophy`, `How To Think` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Grounded answer / abstention contract` and `Retention balance rationale`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Staged traffic shift and automatic abort` and `Privileged production access`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Unpaid leave` and `Joiners, movers and leavers`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Document` connect `Document` to `ChunkerOptions`, `VectorStore`, `StubEmbeddingModel`, `ChatRequest`, `ChatModel`, `PgVectorStore`, `test_api.py`, `.ingest`, `._acquire`, `memory.py`, `ingestion/__init__.py`, `test_server_lifecycle.py`, `Chunk`, `ComponentConfig`, `Reranker`, `conftest.py`, `MemoryVectorStore`, `content_hash`, `recursive.py`, `_FakeEmbeddings`, `_document`, `populated`, `.split`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `ChatRequest` to `Chunk`, `ComponentConfig`, `VectorStore`, `StubEmbeddingModel`, `llm/openai_compatible.py`, `Reranker`, `ChatModel`, `diagnose.py`, `test_langchain_integration.py`, `Container`, `ProviderError`, `grounding.py`, `container.py`, `_FakeEmbeddings`, `answerer.py`, `anthropic_provider.py`, `llm/langchain_bridge.py`, `test_server_lifecycle.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `StubEmbeddingModel` connect `StubEmbeddingModel` to `._encode`, `MemoryVectorStore`, `test_retrieval.py`, `ChatRequest`, `pipeline`, `ChatModel`, `test_cli.py`, `test_api.py`, `PgVectorStore`, `Document`, `_stub_environment`, `populated`, `conftest.py`, `PgVectorOptions`, `test_server_lifecycle.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `MemoryVectorStore` (e.g. with `FailingChatModel` and `NativeCitationChatModel`) actually correct?**
  _`MemoryVectorStore` has 4 INFERRED edges - model-reasoned connections that need verification._