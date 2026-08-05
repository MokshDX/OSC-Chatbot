# Chunker Registration

> 23 nodes

## Key Concepts

- **recursive.py** (21 connections) — `src/osc_assistant/chunking/recursive.py`
- **chunking/__init__.py** (19 connections) — `src/osc_assistant/chunking/__init__.py`
- **to_chunks()** (12 connections) — `src/osc_assistant/chunking/recursive.py`
- **FixedSizeChunker** (7 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **normalize_whitespace()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **_build_recursive()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **_build_fixed()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **_split_keeping_separator()** (4 connections) — `src/osc_assistant/chunking/recursive.py`
- **._split_text()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **_merge()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **_chunk_id()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **register** (2 connections)
- **Chunking strategies. Imported for registration side effects.** (1 connections) — `src/osc_assistant/chunking/__init__.py`
- **Any** (1 connections)
- **Chunking strategies. Chunking is the single highest-leverage retrieval knob and…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Fixed-width character windows with overlap. Ignores document structure…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Split `text` on `separator` without adding or dropping a character.…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Greedily pack pieces up to `chunk_size`, carrying `overlap` characters forward.…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Turn split text into `Chunk`s, denormalising the document's identity onto each.…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **A stable id for a chunk. Content is part of the digest so that an edit which…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Collapse runs of blank lines. Applied by loaders before chunking.** (1 connections) — `src/osc_assistant/chunking/recursive.py`

## Relationships

- [LangChain Text Splitters](LangChain_Text_Splitters.md) (13 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (10 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (6 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (5 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (3 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (2 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (1 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (1 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (1 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (1 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (1 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/__init__.py`
- `src/osc_assistant/chunking/recursive.py`

## Audit Trail

- EXTRACTED: 108 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*