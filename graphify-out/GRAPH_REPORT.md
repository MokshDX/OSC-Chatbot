# Graph Report - .  (2026-07-29)

## Corpus Check
- Corpus is ~23,107 words - fits in a single context window. You may not need a graph.

## Summary
- 812 nodes · 1973 edges · 36 communities (35 shown, 1 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 160 edges (avg confidence: 0.65)
- Token cost: 37,031 input · 10,072 output

## Community Hubs (Navigation)
- In-Memory Store & Noop Reranker
- Corpus Loaders & Ingestion
- Answer Generation & Abstention
- Engineering Handbook & Config Profiles
- HTTP API Layer
- Embedding Model Interface
- Rank Fusion & Citation Grounding
- Chunking Strategies
- Error Hierarchy
- pgvector Store & Integration Tests
- Streaming & Response Types
- Gemini Chat Adapter
- Anthropic Chat Adapter
- Command Line Interface
- HTTP Layer Tests
- OpenAI-Compatible Chat Adapter
- pgvector Search & Migrations
- Settings Loading & YAML Profiles
- Provider Registry
- Vector Store Interface
- Composition Root
- Reranker Interface & Registries
- Hybrid Search Scoring
- Structured Logging
- Dimension Guard & Match Source
- Cross-Encoder Reranker
- Component Config & Registry Tests
- Chat Model Interface
- pgvector Setup & Codecs
- Atomic Document Replacement
- Settings Schema
- Chunker Registration
- OpenAI-Compatible Embeddings
- Provider Package Registration
- Package Entry Point

## God Nodes (most connected - your core abstractions)
1. `StubEmbeddingModel` - 57 edges
2. `MemoryVectorStore` - 50 edges
3. `ComponentConfig` - 46 edges
4. `Document` - 46 edges
5. `ChatRequest` - 39 edges
6. `ScoredChunk` - 32 edges
7. `StubChatModel` - 32 edges
8. `VectorStore` - 31 edges
9. `PgVectorStore` - 31 edges
10. `EmbeddingModel` - 28 edges

## Surprising Connections (you probably didn't know these)
- `Decision Priority Order` --semantically_similar_to--> `One Datastore (PostgreSQL)`  [INFERRED] [semantically similar]
  claude.md → README.md
- `Frozen Prompts` --semantically_similar_to--> `OSC_ Environment Variable Override Convention`  [INFERRED] [semantically similar]
  README.md → config/default.yaml
- `Data Residency / Offline Operation` --semantically_similar_to--> `Not Yet Built (OIDC, ACLs, eval harness)`  [INFERRED] [semantically similar]
  config/experiments/local-only.yaml → README.md
- `client()` --calls--> `create_app()`  [INFERRED]
  tests/test_api.py → src/osc_assistant/api/app.py
- `indexed()` --calls--> `ChunkerOptions`  [INFERRED]
  tests/test_answerer.py → src/osc_assistant/chunking/recursive.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Provider Swappability: protocols, registries, composition root, profiles** — readme_protocol_seams, readme_provider_registry, readme_composition_root, config_default_profile, config_experiments_groq_voyage_profile, config_experiments_local_only_profile [EXTRACTED 1.00]
- **Grounding Guarantee: hybrid retrieval, citations, abstention, frozen prompts** — readme_hybrid_retrieval, readme_native_citations, readme_abstention, readme_frozen_prompts, config_default_generation, claude_minimal_hallucinations_goal [INFERRED 0.85]
- **Single Postgres Backing Store: chunks, vectors, lexical index** — readme_one_datastore, readme_vectorstore, config_default_vector_store, config_default_database, docker_compose_postgres_service [INFERRED 0.95]

## Communities (36 total, 1 thin omitted)

### Community 0 - "In-Memory Store & Noop Reranker"
Cohesion: 0.07
Nodes (46): NoopReranker, Truncates the candidate list without reordering it., MemoryVectorStore, A dictionary-backed `VectorStore`., Replace a document and its chunks. Atomic by construction: the vectors are…, documents(), embeddings(), fixture (+38 more)

### Community 1 - "Corpus Loaders & Ingestion"
Cohesion: 0.07
Nodes (42): normalize_whitespace(), Collapse runs of blank lines. Applied by loaders before chunking., Corpus ingestion: connectors and the chunk/embed/store pipeline., _derive_title(), FilesystemLoader, InMemoryLoader, Path, Corpus connectors. A loader is any object with `load() ->… (+34 more)

### Community 2 - "Answer Generation & Abstention"
Cohesion: 0.07
Nodes (29): AnswerEvent, AnswerComplete, Answerer, Apply the citation policy and assemble the final answer., Emitted before generation so the client can render sources immediately., The authoritative final answer., Answers a question against the indexed corpus., Answer `question`, returning the complete result. (+21 more)

### Community 3 - "Engineering Handbook & Config Profiles"
Cohesion: 0.07
Nodes (45): Decision Priority Order, Dependency Policy, Documentation As First-Class Deliverable, Engineering Philosophy (correct, reliable, maintainable), Minimal Hallucinations Project Goal, Modular, Loosely Coupled Architecture Standard, OSC Engineering Handbook, Testing Policy (deterministic, failure-path) (+37 more)

### Community 4 - "HTTP API Layer"
Cohesion: 0.09
Nodes (36): FastAPI, get, post, Request, chat(), _container(), create_app(), health() (+28 more)

### Community 5 - "Embedding Model Interface"
Cohesion: 0.05
Nodes (22): EmbeddingModel, A text embedding model. Document and query embedding are separate methods…, Vector width. Must match the vector store's configured dimension., Embed corpus text. Returns one vector per input, in order., Embed a search query., _build(), GeminiEmbeddingModel, register (+14 more)

### Community 6 - "Rank Fusion & Citation Grounding"
Cohesion: 0.08
Nodes (39): Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…, Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…, reciprocal_rank_fusion(), _escape(), parse_marker_citations(), Escape the characters that would otherwise break out of an XML-ish attribute., Render sources as a delimited block for inclusion in a prompt. The delimiter…, Extract citations from `[n]` markers in `text`. Markers referring to a source… (+31 more)

### Community 7 - "Chunking Strategies"
Cohesion: 0.10
Nodes (33): Chunking strategies. Imported for registration side effects., _chunk_id(), ChunkerOptions, FixedSizeChunker, _merge(), BaseModel, Split `text` on `separator` without adding or dropping a character.…, Greedily pack pieces up to `chunk_size`, carrying `overlap` characters forward.… (+25 more)

### Community 8 - "Error Hierarchy"
Cohesion: 0.09
Nodes (27): Exception, AssistantError, ConfigurationError, MissingDependencyError, ProviderError, Exception hierarchy for the assistant. A single root (`AssistantError`) lets…, Base class for every error raised by this package., The system is misconfigured and cannot start or serve a request. Raised for… (+19 more)

### Community 9 - "pgvector Store & Integration Tests"
Cohesion: 0.10
Nodes (24): PgVectorOptions, PgVectorStore, BaseModel, Adapter over PostgreSQL with the pgvector extension., The partition this store reads and writes. Every query is scoped to it., Integration tests for the PostgreSQL store. Skipped unless `OSC_TEST_DSN`…, Chunk ids incorporate content, so an edit yields new ids. Without the delete…, The skip check reads a recorded hash as "chunks are present". A partial write… (+16 more)

### Community 10 - "Streaming & Response Types"
Cohesion: 0.12
Nodes (16): StreamEvent, Stream text, resolving citations from the accumulated answer at the end.…, ChatResponse, Citation, CitationDelta, A reference from the answer back to the material that supports it. `index` is…, An incremental fragment of the answer., A citation resolved mid-stream. (+8 more)

### Community 11 - "Gemini Chat Adapter"
Cohesion: 0.13
Nodes (19): compose_grounded_system(), Grounding and citation handling for providers without native citation support.…, Fold the system prompt, citation instruction and sources into one string. Used…, _build(), _build_contents(), _finish_reason(), GeminiChatModel, GeminiOptions (+11 more)

### Community 12 - "Anthropic Chat Adapter"
Cohesion: 0.14
Nodes (16): AnthropicChatModel, AnthropicOptions, _build(), _build_messages(), _last_user_index(), _parse_content(), _parse_usage(), Any (+8 more)

### Community 13 - "Command Line Interface"
Cohesion: 0.21
Nodes (18): Argument, command, help, Option, ProfileOption, ask(), ingest(), providers() (+10 more)

### Community 14 - "HTTP Layer Tests"
Cohesion: 0.16
Nodes (18): TestClient, client(), _parse_sse(), fixture, parametrize, HTTP layer tests. These run the real application — real container, real…, Validation happens at the trust boundary, before any provider is touched., Decode a server-sent event stream into (event name, payload) pairs. (+10 more)

### Community 15 - "OpenAI-Compatible Chat Adapter"
Cohesion: 0.15
Nodes (12): Chat model providers. Imported for registration side effects., _make_factory(), OpenAICompatibleChatModel, OpenAICompatibleOptions, _parse_usage(), _Preset, Any, BaseModel (+4 more)

### Community 16 - "pgvector Search & Migrations"
Cohesion: 0.19
Nodes (8): _encode_vector(), Any, Vector, Replace a document and its chunks in a single transaction. Delete-then-insert…, Apply unapplied migration files in filename order. A hand-rolled runner rather…, Fail loudly if the stored vector width disagrees with the active model.…, Render a vector in pgvector's literal form for the `::vector` cast., _to_scored_chunk()

### Community 17 - "Settings Loading & YAML Profiles"
Cohesion: 0.18
Nodes (10): BaseSettings, PydanticBaseSettingsSource, OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…, load_settings(), Any, Lowest-precedence source reading a YAML profile. The profile path comes from…, Build settings, applying `overrides` at the highest precedence., Root configuration object. Nested values are addressable from the environment… (+2 more)

### Community 18 - "Provider Registry"
Cohesion: 0.16
Nodes (10): Factory, A component was requested by a name that is not registered., UnknownComponentError, Maps a provider name to a factory for one kind of component., Decorator registering a factory under `name`. Re-registering a name replaces…, Registry, T, parametrize (+2 more)

### Community 19 - "Vector Store Interface"
Cohesion: 0.13
Nodes (8): Remove a document and every chunk belonging to it., Map document id to stored content hash, for incremental sync., Every document id currently indexed., Lexical search. Return `[]` if the store has no lexical index., Persistence and retrieval of embedded chunks. Implementations that cannot do…, Prepare the store (connect, create collections). Idempotent., The vector width this store is configured to hold., VectorStore

### Community 20 - "Composition Root"
Cohesion: 0.16
Nodes (5): Self, Container, A cheaper model for auxiliary steps such as query rewriting., Builds and owns the application's components., Build the store, injecting values it cannot know on its own. Vector width, the…

### Community 21 - "Reranker Interface & Registries"
Cohesion: 0.18
Nodes (8): A second-stage relevance model applied to retrieval candidates., Return the `top_k` most relevant candidates, most relevant first., Reranker, _build(), register, Pass-through reranker: the default. Reranking is a real accuracy gain but costs…, The registries for every swappable component. Kept in one small module so that…, A minimal registry so new providers are additions, never edits. This exists to…

### Community 22 - "Hybrid Search Scoring"
Cohesion: 0.22
Nodes (8): Vector, Combined lexical and vector search, fused into a single ranking., _cosine_similarity(), Vector, Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…, _tokenize(), A chunk with a relevance score. Scores are only comparable within a single…, ScoredChunk

### Community 23 - "Structured Logging"
Cohesion: 0.20
Nodes (9): Logger, LogRecord, Composition root. The only module that knows both which providers exist and how…, configure_logging(), get_logger(), JsonFormatter, Structured logging. Answers must be auditable: which chunks were retrieved,…, Renders records as single-line JSON. (+1 more)

### Community 24 - "Dimension Guard & Match Source"
Cohesion: 0.17
Nodes (8): DimensionMismatchError, The configured embedding model does not match the store's vector width.…, _build(), register, In-process vector store. Not a toy: this is what makes the test suite run…, MatchSource, Where a retrieval hit came from. Recorded for tracing and evaluation., StrEnum

### Community 25 - "Cross-Encoder Reranker"
Cohesion: 0.20
Nodes (7): _build(), CrossEncoderOptions, CrossEncoderReranker, BaseModel, register, Local cross-encoder reranker. A cross-encoder scores the query and candidate…, Adapter over a `sentence-transformers` CrossEncoder.

### Community 26 - "Component Config & Registry Tests"
Cohesion: 0.23
Nodes (11): ComponentConfig, BaseModel, Selects and configures one swappable component. `options` is intentionally…, The registry is the mechanism that makes providers pluggable, so it is tested…, Overriding a built-in must be possible without editing it., A typo in a profile must fail loudly rather than be silently ignored., test_options_are_passed_through_untouched(), test_re_registration_overrides() (+3 more)

### Community 27 - "Chat Model Interface"
Cohesion: 0.18
Nodes (7): ChatModel, StreamEvent, A text-generating model., The provider's identifier for the underlying model, for logs and traces., True if the provider resolves citations itself from structured sources. When…, Generate a complete response., Generate a response incrementally.

### Community 28 - "pgvector Setup & Codecs"
Cohesion: 0.22
Nodes (8): The vector store could not complete an operation., VectorStoreError, _build(), register, PostgreSQL + pgvector store: the production default. One datastore holds chunk…, Open the pool and, unless disabled, apply pending migrations., Decode JSONB into Python objects instead of raw strings., _register_codecs()

### Community 29 - "Atomic Document Replacement"
Cohesion: 0.22
Nodes (9): Atomically replace a document and all of its chunks. Must be all-or-nothing.…, Chunk, EmbeddedChunk, A retrievable span of a document. `title` and `source_uri` are denormalised…, A chunk paired with the vector produced for it, tagged with its model. The…, populated(), fixture, Mixing vector widths silently produces nonsense scores; it must raise. (+1 more)

### Community 30 - "Settings Schema"
Cohesion: 0.33
Nodes (9): ChunkingSettings, DatabaseSettings, GenerationSettings, BaseModel, Configuration. Layered, highest precedence first: process environment, then…, Tuning for the retrieval stage. Every value here is an experiment knob., RetrievalSettings, ServerSettings (+1 more)

### Community 31 - "Chunker Registration"
Cohesion: 0.31
Nodes (7): Protocol, _build_fixed(), _build_recursive(), register, Chunking strategies. Chunking is the single highest-leverage retrieval knob and…, Chunker, Splits a document into retrievable units.

### Community 32 - "OpenAI-Compatible Embeddings"
Cohesion: 0.39
Nodes (3): OpenAICompatibleEmbeddingModel, Vector, Adapter over the `/v1/embeddings` interface.

### Community 33 - "Provider Package Registration"
Cohesion: 0.33
Nodes (3): Provider implementations. Importing this package registers every built-in…, Reranker providers. Imported for registration side effects., Vector store providers. Imported for registration side effects.

## Knowledge Gaps
- **1 isolated node(s):** `osc-assistant`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ComponentConfig` connect `Component Config & Registry Tests` to `Embedding Model Interface`, `Error Hierarchy`, `Gemini Chat Adapter`, `Anthropic Chat Adapter`, `OpenAI-Compatible Chat Adapter`, `Settings Loading & YAML Profiles`, `Provider Registry`, `Composition Root`, `Reranker Interface & Registries`, `Structured Logging`, `Dimension Guard & Match Source`, `Cross-Encoder Reranker`, `pgvector Setup & Codecs`, `Settings Schema`, `Chunker Registration`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `Document` connect `Corpus Loaders & Ingestion` to `In-Memory Store & Noop Reranker`, `Embedding Model Interface`, `Chunking Strategies`, `Error Hierarchy`, `pgvector Store & Integration Tests`, `Streaming & Response Types`, `HTTP Layer Tests`, `pgvector Search & Migrations`, `Vector Store Interface`, `Reranker Interface & Registries`, `Dimension Guard & Match Source`, `Chat Model Interface`, `pgvector Setup & Codecs`, `Atomic Document Replacement`, `Chunker Registration`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `StubEmbeddingModel` connect `In-Memory Store & Noop Reranker` to `Corpus Loaders & Ingestion`, `pgvector Store & Integration Tests`, `Streaming & Response Types`, `Gemini Chat Adapter`, `HTTP Layer Tests`, `Atomic Document Replacement`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `StubEmbeddingModel` (e.g. with `MemoryVectorStore` and `ChatRequest`) actually correct?**
  _`StubEmbeddingModel` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `MemoryVectorStore` (e.g. with `FailingChatModel` and `NativeCitationChatModel`) actually correct?**
  _`MemoryVectorStore` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ComponentConfig` (e.g. with `Container` and `UnknownComponentError`) actually correct?**
  _`ComponentConfig` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Document` (e.g. with `ChatModel` and `Chunker`) actually correct?**
  _`Document` has 9 INFERRED edges - model-reasoned connections that need verification._