# RRF Fusion & Source Rendering

> 34 nodes · cohesion 0.10

## Key Concepts

- **test_fusion_and_grounding.py** (23 connections) — `tests/test_fusion_and_grounding.py`
- **reciprocal_rank_fusion()** (11 connections) — `src/osc_assistant/fusion.py`
- **render_sources()** (10 connections) — `src/osc_assistant/grounding.py`
- **_sources()** (9 connections) — `tests/test_fusion_and_grounding.py`
- **_ranking()** (8 connections) — `tests/test_fusion_and_grounding.py`
- **test_answer_without_markers_has_no_citations()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_delimiter_differs_between_requests()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_keeps_chunks_found_by_only_one_ranking()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_rewards_agreement_between_rankings()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_out_of_range_markers_are_ignored()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_titles_cannot_break_out_of_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_source_bodies_cannot_close_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **_escape()** (3 connections) — `src/osc_assistant/grounding.py`
- **_chunk()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_citations_are_ordered_by_first_appearance()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_deduplicates()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_marks_results_as_hybrid()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_respects_the_limit()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_markers_resolve_to_the_matching_source()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_sources_are_numbered_from_one()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_repeated_markers_produce_one_citation()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_of_nothing_is_empty()** (2 connections) — `tests/test_fusion_and_grounding.py`
- **test_no_sources_renders_nothing()** (2 connections) — `tests/test_fusion_and_grounding.py`
- **Fuse several rankings of the same corpus into one. Args: rankings: Rankings to…** (1 connections) — `src/osc_assistant/fusion.py`
- **Escape the characters that would otherwise break out of an XML-ish attribute.** (1 connections) — `src/osc_assistant/grounding.py`
- *... and 9 more nodes in this community*

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (5 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (4 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (3 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (3 shared connections)
- [Citation Grounding & Reasoning Models](Citation_Grounding_%26_Reasoning_Models.md) (3 shared connections)
- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (1 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (1 shared connections)

## Source Files

- `src/osc_assistant/fusion.py`
- `src/osc_assistant/grounding.py`
- `tests/test_fusion_and_grounding.py`

## Audit Trail

- EXTRACTED: 131 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*