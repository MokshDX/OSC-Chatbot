# Anthropic Adapter & Retrieval Pipeline

> 29 nodes · cohesion 0.11

## Key Concepts

- **anthropic_provider.py** (27 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **SourceDocument** (15 connections) — `src/osc_assistant/types.py`
- **.stream()** (11 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicChatModel** (10 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.complete()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build_messages()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_parse_content()** (7 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **._build_payload()** (6 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_parse_usage()** (5 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Any** (5 connections)
- **.__init__()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **AnthropicOptions** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **_last_user_index()** (3 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.as_sources()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.aclose()** (2 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.model_id()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **.supports_citations()** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **BaseModel** (1 connections)
- **register** (1 connections)
- **StreamEvent** (1 connections)
- **Anthropic chat provider. This is the only adapter with native citation support:…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Stream the answer, then emit citations once the message is complete. Text is…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Attach sources as citable documents on the final user turn. Sources belong to…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- **Flatten response blocks into text, appending a marker after each cited span.…** (1 connections) — `src/osc_assistant/providers/llm/anthropic_provider.py`
- *... and 4 more nodes in this community*

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (13 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (7 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (6 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (4 shared connections)
- [RRF Fusion & Source Rendering](RRF_Fusion_%26_Source_Rendering.md) (4 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (3 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (2 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (2 shared connections)
- [Citation Grounding & Reasoning Models](Citation_Grounding_%26_Reasoning_Models.md) (2 shared connections)
- [OpenAI-Compatible Chat Provider](OpenAI-Compatible_Chat_Provider.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/llm/anthropic_provider.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 130 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*