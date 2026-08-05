# Rank Fusion & Source Rendering

> 42 nodes

## Key Concepts

- **test_fusion_and_grounding.py** (23 connections) — `tests/test_fusion_and_grounding.py`
- **SourceDocument** (15 connections) — `src/osc_assistant/types.py`
- **reciprocal_rank_fusion()** (11 connections) — `src/osc_assistant/fusion.py`
- **render_sources()** (10 connections) — `src/osc_assistant/grounding.py`
- **_sources()** (9 connections) — `tests/test_fusion_and_grounding.py`
- **_ranking()** (8 connections) — `tests/test_fusion_and_grounding.py`
- **fusion.py** (7 connections) — `src/osc_assistant/fusion.py`
- **test_reasoning_markers_never_become_citations()** (5 connections) — `tests/test_reasoning_models.py`
- **test_fusion_rewards_agreement_between_rankings()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_keeps_chunks_found_by_only_one_ranking()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_out_of_range_markers_are_ignored()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_answer_without_markers_has_no_citations()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_titles_cannot_break_out_of_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_source_bodies_cannot_close_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_delimiter_differs_between_requests()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **_escape()** (3 connections) — `src/osc_assistant/grounding.py`
- **.as_sources()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **_chunk()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_deduplicates()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_marks_results_as_hybrid()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_respects_the_limit()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_markers_resolve_to_the_matching_source()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_repeated_markers_produce_one_citation()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_citations_are_ordered_by_first_appearance()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_sources_are_numbered_from_one()** (3 connections) — `tests/test_fusion_and_grounding.py`
- *... and 17 more nodes in this community*

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (7 shared connections)
- [Grounding & OpenAI-Compatible Chat](Grounding_%26_OpenAI-Compatible_Chat.md) (6 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (3 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (3 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (3 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (3 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (2 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (1 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (1 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (1 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)

## Source Files

- `src/osc_assistant/fusion.py`
- `src/osc_assistant/grounding.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/types.py`
- `tests/test_fusion_and_grounding.py`
- `tests/test_reasoning_models.py`

## Audit Trail

- EXTRACTED: 162 (98%)
- INFERRED: 3 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*