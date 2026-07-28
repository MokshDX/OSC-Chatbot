# Rank Fusion & Citation Grounding

> 42 nodes · cohesion 0.08

## Key Concepts

- **test_fusion_and_grounding.py** (23 connections) — `tests/test_fusion_and_grounding.py`
- **parse_marker_citations()** (17 connections) — `src/osc_assistant/grounding.py`
- **SourceDocument** (13 connections) — `src/osc_assistant/types.py`
- **reciprocal_rank_fusion()** (11 connections) — `src/osc_assistant/fusion.py`
- **render_sources()** (10 connections) — `src/osc_assistant/grounding.py`
- **_sources()** (9 connections) — `tests/test_fusion_and_grounding.py`
- **_ranking()** (8 connections) — `tests/test_fusion_and_grounding.py`
- **fusion.py** (7 connections) — `src/osc_assistant/fusion.py`
- **test_answer_without_markers_has_no_citations()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_delimiter_differs_between_requests()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_keeps_chunks_found_by_only_one_ranking()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_rewards_agreement_between_rankings()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_out_of_range_markers_are_ignored()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_titles_cannot_break_out_of_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **test_source_bodies_cannot_close_the_delimiter()** (4 connections) — `tests/test_fusion_and_grounding.py`
- **_escape()** (3 connections) — `src/osc_assistant/grounding.py`
- **.as_sources()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **_chunk()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_citations_are_ordered_by_first_appearance()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_deduplicates()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_marks_results_as_hybrid()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_fusion_respects_the_limit()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_markers_resolve_to_the_matching_source()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_rendered_sources_are_numbered_from_one()** (3 connections) — `tests/test_fusion_and_grounding.py`
- **test_repeated_markers_produce_one_citation()** (3 connections) — `tests/test_fusion_and_grounding.py`
- *... and 17 more nodes in this community*

## Relationships

- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (10 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (4 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (4 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (3 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (3 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (3 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)
- [OpenAI-Compatible Chat Adapter](OpenAI-Compatible_Chat_Adapter.md) (1 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (1 shared connections)

## Source Files

- `src/osc_assistant/fusion.py`
- `src/osc_assistant/grounding.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/types.py`
- `tests/test_fusion_and_grounding.py`

## Audit Trail

- EXTRACTED: 173 (99%)
- INFERRED: 2 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*