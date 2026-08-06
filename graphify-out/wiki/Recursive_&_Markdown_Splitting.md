# Recursive & Markdown Splitting

> 25 nodes · cohesion 0.10

## Key Concepts

- **recursive.py** (21 connections) — `src/osc_assistant/chunking/recursive.py`
- **to_chunks()** (12 connections) — `src/osc_assistant/chunking/recursive.py`
- **MarkdownChunker** (10 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **LangChainRecursiveChunker** (9 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **FixedSizeChunker** (7 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/recursive.py`
- **_build_fixed()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **_build_recursive()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (4 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_split_keeping_separator()** (4 connections) — `src/osc_assistant/chunking/recursive.py`
- **_chunk_id()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **_merge()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **._split_text()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **register** (2 connections)
- **Heading-aware splitting: structure first, then size. Two passes, because either…** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **`RecursiveCharacterTextSplitter` behind the OSC `Chunker` protocol.** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Any** (1 connections)
- **Chunking strategies. Chunking is the single highest-leverage retrieval knob and…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Split `text` on `separator` without adding or dropping a character.…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Greedily pack pieces up to `chunk_size`, carrying `overlap` characters forward.…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Turn split text into `Chunk`s, denormalising the document's identity onto each.…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **A stable id for a chunk. Content is part of the digest so that an edit which…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Fixed-width character windows with overlap. Ignores document structure…** (1 connections) — `src/osc_assistant/chunking/recursive.py`

## Relationships

- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (14 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (12 shared connections)
- [LangChain Bridges & Splitters](LangChain_Bridges_%26_Splitters.md) (9 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (6 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (6 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (3 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (1 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/langchain_splitters.py`
- `src/osc_assistant/chunking/recursive.py`

## Audit Trail

- EXTRACTED: 106 (93%)
- INFERRED: 8 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*