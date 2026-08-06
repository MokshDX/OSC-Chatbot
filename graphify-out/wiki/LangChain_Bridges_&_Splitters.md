# LangChain Bridges & Splitters

> 61 nodes · cohesion 0.05

## Key Concepts

- **test_langchain_integration.py** (40 connections) — `tests/test_langchain_integration.py`
- **LangChainChunkerOptions** (14 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_document()** (11 connections) — `tests/test_langchain_integration.py`
- **_bridge()** (9 connections) — `tests/test_langchain_integration.py`
- **langchain.py** (7 connections) — `src/osc_assistant/integrations/langchain.py`
- **_embedding_bridge()** (7 connections) — `tests/test_langchain_integration.py`
- **OSCRetriever()** (6 connections) — `src/osc_assistant/integrations/langchain.py`
- **LangChainChatOptions** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **_require_splitters()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **test_bridge_reports_an_empty_completion_rather_than_abstaining()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_streams_text_then_citations()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_strips_a_leaked_reasoning_block()** (5 connections) — `tests/test_langchain_integration.py`
- **test_chunk_ids_are_stable_across_runs()** (5 connections) — `tests/test_langchain_integration.py`
- **test_chunking_preserves_document_content()** (5 connections) — `tests/test_langchain_integration.py`
- **test_langchain_recursive_respects_the_size_budget()** (5 connections) — `tests/test_langchain_integration.py`
- **test_markdown_chunker_keeps_headings_in_the_chunk_text()** (5 connections) — `tests/test_langchain_integration.py`
- **test_markdown_chunker_records_the_heading_path()** (5 connections) — `tests/test_langchain_integration.py`
- **test_the_langchain_retriever_refuses_the_synchronous_path()** (5 connections) — `tests/test_langchain_integration.py`
- **test_unbroken_text_is_still_split()** (5 connections) — `tests/test_langchain_integration.py`
- **_heading_path()** (4 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **to_langchain_document()** (4 connections) — `src/osc_assistant/integrations/langchain.py`
- **.embed_documents()** (4 connections) — `tests/test_langchain_integration.py`
- **.embed_query()** (4 connections) — `tests/test_langchain_integration.py`
- **parametrize** (4 connections)
- **test_bridge_translates_a_completion_and_parses_citations()** (4 connections) — `tests/test_langchain_integration.py`
- *... and 36 more nodes in this community*

## Relationships

- [Recursive & Markdown Splitting](Recursive_%26_Markdown_Splitting.md) (9 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (8 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (7 shared connections)
- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (6 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (5 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (4 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (4 shared connections)
- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (3 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (3 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (2 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (2 shared connections)

## Source Files

- `src/osc_assistant/chunking/langchain_splitters.py`
- `src/osc_assistant/integrations/langchain.py`
- `src/osc_assistant/providers/llm/langchain_bridge.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 223 (91%)
- INFERRED: 23 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*