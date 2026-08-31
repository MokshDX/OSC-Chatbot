# Regression Gate Tests

> 38 nodes

## Key Concepts

- **test_fusion_and_grounding.py** (23 connections) — `tests/test_fusion_and_grounding.py`
- **parse_marker_citations()** (21 connections) — `src/osc_assistant/grounding.py`
- **SourceDocument** (15 connections) — `src/osc_assistant/types.py`
- **reciprocal_rank_fusion()** (11 connections) — `src/osc_assistant/fusion.py`
- **render_sources()** (10 connections) — `src/osc_assistant/grounding.py`
- **_sources()** (9 connections) — `tests/test_fusion_and_grounding.py`
- **_ranking()** (8 connections) — `tests/test_fusion_and_grounding.py`
- **test_reasoning_markers_never_become_citations()** (5 connections) — `tests/test_reasoning_models.py`
- **test_fusion_rewards_agreement_between_rankings()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_keeps_chunks_found_by_only_one_ranking()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_out_of_range_markers_are_ignored()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_answer_without_markers_has_no_citations()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_titles_cannot_break_out_of_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_source_bodies_cannot_close_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_delimiter_differs_between_requests()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **_chunk()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_deduplicates()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_marks_results_as_hybrid()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_respects_the_limit()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_markers_resolve_to_the_matching_source()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_repeated_markers_produce_one_citation()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_citations_are_ordered_by_first_appearance()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_sources_are_numbered_from_one()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_of_nothing_is_empty()** (2 connections) — `tests/test_fusion_and_grounding.py`
- **test_no_sources_renders_nothing()** (2 connections) — `tests/test_fusion_and_grounding.py`
- *... and 13 more nodes in this community*

## Relationships

- [VectorStore Protocol](VectorStore_Protocol.md) (7 shared connections)
- [Logging System Design](Logging_System_Design.md) (4 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (4 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (3 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (3 shared connections)
- [Logging Tests](Logging_Tests.md) (3 shared connections)
- [Chunker Registration](Chunker_Registration.md) (3 shared connections)
- [Conversation Turn Orchestration](Conversation_Turn_Orchestration.md) (3 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (1 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (1 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (1 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (1 shared connections)

## Source Files

- `src/osc_assistant/fusion.py`
- `src/osc_assistant/grounding.py`
- `src/osc_assistant/types.py`
- `tests/test_fusion_and_grounding.py`
- `tests/test_reasoning_models.py`

## Audit Trail

- EXTRACTED: 166 (97%)
- INFERRED: 5 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*