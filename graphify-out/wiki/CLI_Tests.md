# CLI Tests

> 20 nodes

## Key Concepts

- **test_cli.py** (42 connections) — `tests/test_cli.py`
- **test_config_reports_the_resolved_values_and_their_source()** (1 connections) — `tests/test_cli.py`
- **test_config_shows_secrets_when_asked()** (1 connections) — `tests/test_cli.py`
- **test_config_emits_json()** (1 connections) — `tests/test_cli.py`
- **test_providers_marks_the_active_selection()** (1 connections) — `tests/test_cli.py`
- **test_providers_emits_json()** (1 connections) — `tests/test_cli.py`
- **test_status_reports_an_empty_index_without_dividing_by_zero()** (1 connections) — `tests/test_cli.py`
- **test_status_emits_json()** (1 connections) — `tests/test_cli.py`
- **test_documents_reports_an_empty_index_plainly()** (1 connections) — `tests/test_cli.py`
- **test_an_unknown_document_fails_with_a_useful_message()** (1 connections) — `tests/test_cli.py`
- **test_an_unknown_chunk_fails_with_a_useful_message()** (1 connections) — `tests/test_cli.py`
- **test_ask_abstains_against_an_empty_index()** (1 connections) — `tests/test_cli.py`
- **test_ask_emits_json()** (1 connections) — `tests/test_cli.py`
- **test_search_explain_prints_the_stages_it_ran()** (1 connections) — `tests/test_cli.py`
- **test_trace_accepts_an_id_prefix()** (1 connections) — `tests/test_cli.py`
- **test_traces_can_be_filtered_by_outcome_and_duration()** (1 connections) — `tests/test_cli.py`
- **test_traces_reports_an_empty_log_plainly()** (1 connections) — `tests/test_cli.py`
- **test_an_unknown_trace_id_fails_with_a_useful_message()** (1 connections) — `tests/test_cli.py`
- **test_version_reports_the_versions_that_shape_behaviour()** (1 connections) — `tests/test_cli.py`
- **CLI tests. The operational commands are the primary interface for anyone…** (1 connections) — `tests/test_cli.py`

## Relationships

- [Path](Path.md) (6 shared connections)
- [_stub_environment()](_stub_environment%28%29.md) (3 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (1 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (1 shared connections)
- [Settings Schema](Settings_Schema.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (1 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (1 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (1 shared connections)
- [test_ask_explain_prints_the_execution_trace()](test_ask_explain_prints_the_execution_trace%28%29.md) (1 shared connections)
- [test_config_redacts_credentials_by_default()](test_config_redacts_credentials_by_default%28%29.md) (1 shared connections)
- [test_help_groups_commands_by_purpose()](test_help_groups_commands_by_purpose%28%29.md) (1 shared connections)

## Source Files

- `tests/test_cli.py`

## Audit Trail

- EXTRACTED: 61 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*