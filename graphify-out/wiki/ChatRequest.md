# ChatRequest

> God node · 57 connections · `src/osc_assistant/types.py`

**Community:** [LangChain Integration Tests](LangChain_Integration_Tests.md)

## Connections by Relation

### calls
- .is_faithful() `EXTRACTED`
- .rewrite() `EXTRACTED`
- test_bridge_reports_an_empty_completion_rather_than_abstaining() `EXTRACTED`
- test_bridge_streams_text_then_citations() `EXTRACTED`
- test_bridge_strips_a_leaked_reasoning_block() `EXTRACTED`
- test_bridge_translates_a_completion_and_parses_citations() `EXTRACTED`

### contains
- types.py `EXTRACTED`

### imports
- protocols.py `EXTRACTED`
- answerer.py `EXTRACTED`
- llm/langchain_bridge.py `EXTRACTED`
- llm/openai_compatible.py `EXTRACTED`
- llm/gemini.py `EXTRACTED`
- anthropic_provider.py `EXTRACTED`
- grounding.py `EXTRACTED`
- judge.py `EXTRACTED`
- rewrite.py `EXTRACTED`

### rationale_for
- A provider-neutral generation request. `sources`, when present, is grounding… `EXTRACTED`

### references
- .stream() `EXTRACTED`
- .stream() `EXTRACTED`
- .stream() `EXTRACTED`
- .complete() `EXTRACTED`
- .stream() `EXTRACTED`
- compose_grounded_system() `EXTRACTED`
- .complete() `EXTRACTED`
- .complete() `EXTRACTED`
- .stream() `EXTRACTED`
- .stream() `EXTRACTED`
- .complete() `EXTRACTED`
- ._build_config() `EXTRACTED`
- _to_langchain_messages() `EXTRACTED`
- .stream() `EXTRACTED`
- ._build_request() `EXTRACTED`
- ._build_payload() `EXTRACTED`
- _build_contents() `EXTRACTED`
- ._bind() `EXTRACTED`
- ._build_payload() `EXTRACTED`
- .complete() `EXTRACTED`

### uses
- [StubEmbeddingModel](StubEmbeddingModel.md) `INFERRED`
- StubChatModel `INFERRED`
- EmbeddingModel `INFERRED`
- VectorStore `INFERRED`
- ChatModel `INFERRED`
- _FakeEmbeddings `INFERRED`
- _ExplodingChatModel `INFERRED`
- _SyncClosableReranker `INFERRED`
- Chunker `INFERRED`
- _ClosableEmbedding `INFERRED`
- Reranker `INFERRED`
- NativeCitationChatModel `INFERRED`
- FailingChatModel `INFERRED`
- StoreInspector `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*