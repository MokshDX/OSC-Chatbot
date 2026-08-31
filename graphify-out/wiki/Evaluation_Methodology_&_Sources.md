# Evaluation Methodology & Sources

> 20 nodes

## Key Concepts

- **test_cli.py** (38 connections) — `tests/test_cli.py`
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

- [Doctor Command Tests](Doctor_Command_Tests.md) (6 shared connections)
- [CLI Failure Reporting Tests](CLI_Failure_Reporting_Tests.md) (3 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (1 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)
- [Explain Flag Test](Explain_Flag_Test.md) (1 shared connections)
- [Config Redaction Test](Config_Redaction_Test.md) (1 shared connections)
- [Help Grouping Test](Help_Grouping_Test.md) (1 shared connections)
- [Unreachable Service Test](Unreachable_Service_Test.md) (1 shared connections)
- [Most-Recent Trace Test](Most-Recent_Trace_Test.md) (1 shared connections)
- [Cross-Process Trace Test](Cross-Process_Trace_Test.md) (1 shared connections)
- [Trace Name Filter Test](Trace_Name_Filter_Test.md) (1 shared connections)

## Source Files

- `tests/test_cli.py`

## Audit Trail

- EXTRACTED: 57 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*