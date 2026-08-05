# IndexStatistics

> 6 nodes

## Key Concepts

- **IndexStatistics** (16 connections) — `src/osc_assistant/types.py`
- **.from_domain()** (3 connections) — `src/osc_assistant/api/schemas.py`
- **.statistics()** (3 connections) — `src/osc_assistant/protocols.py`
- **.statistics()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Corpus-wide counts and chunk-size distribution.** (1 connections) — `src/osc_assistant/protocols.py`
- **Aggregate state of the index. Chunk length percentiles are here because chunk…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [HTTP API Layer](HTTP_API_Layer.md) (3 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (3 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (2 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (2 shared connections)
- [pgvector Store Interface](pgvector_Store_Interface.md) (1 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (1 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (1 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (1 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (1 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/schemas.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 21 (78%)
- INFERRED: 6 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*