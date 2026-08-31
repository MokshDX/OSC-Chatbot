# In-Memory Session Store

> 31 nodes

## Key Concepts

- **test_logging.py** (40 connections) — `tests/test_logging.py`
- **Path** (36 connections)
- **_records()** (30 connections) — `tests/test_logging.py`
- **test_every_record_inside_a_trace_carries_its_trace_id()** (4 connections) — `tests/test_logging.py`
- **test_each_pipeline_stage_logs_once_at_trace_level()** (4 connections) — `tests/test_logging.py`
- **test_third_party_debug_output_is_pinned_out_of_our_stream()** (4 connections) — `tests/test_logging.py`
- **test_a_log_file_is_created_and_records_land_in_it()** (3 connections) — `tests/test_logging.py`
- **test_the_directory_is_created_if_it_does_not_exist()** (3 connections) — `tests/test_logging.py`
- **test_records_below_the_configured_level_are_not_written()** (3 connections) — `tests/test_logging.py`
- **test_trace_is_a_real_level_below_debug()** (3 connections) — `tests/test_logging.py`
- **test_an_explicit_trace_id_on_the_call_site_is_not_overwritten()** (3 connections) — `tests/test_logging.py`
- **test_span_logging_costs_nothing_when_the_level_excludes_it()** (3 connections) — `tests/test_logging.py`
- **test_span_logging_can_be_disabled_outright()** (3 connections) — `tests/test_logging.py`
- **test_a_failing_stage_still_logs_its_span_with_the_error()** (3 connections) — `tests/test_logging.py`
- **test_corpus_text_is_reduced_to_a_length_by_default()** (3 connections) — `tests/test_logging.py`
- **test_payload_capture_restores_the_text()** (3 connections) — `tests/test_logging.py`
- **test_redaction_applies_to_the_console_as_well_as_the_file()** (3 connections) — `tests/test_logging.py`
- **test_audit_records_go_to_their_own_file()** (3 connections) — `tests/test_logging.py`
- **test_an_exception_is_recorded_with_its_traceback()** (3 connections) — `tests/test_logging.py`
- **test_shutdown_is_idempotent_and_leaks_no_listener()** (3 connections) — `tests/test_logging.py`
- **test_file_logging_is_off_when_no_directory_is_configured()** (2 connections) — `tests/test_logging.py`
- **test_the_log_rotates_at_the_configured_size()** (2 connections) — `tests/test_logging.py`
- **test_disk_stays_under_the_configured_ceiling()** (2 connections) — `tests/test_logging.py`
- **test_audit_can_be_disabled()** (2 connections) — `tests/test_logging.py`
- **test_the_audit_stream_has_its_own_retention()** (2 connections) — `tests/test_logging.py`
- *... and 6 more nodes in this community*

## Relationships

- [CLI Settings Bootstrap](CLI_Settings_Bootstrap.md) (9 shared connections)
- [Credential Redaction Tests](Credential_Redaction_Tests.md) (6 shared connections)
- [Log Retention Tests](Log_Retention_Tests.md) (4 shared connections)
- [Unserialisable Value Test](Unserialisable_Value_Test.md) (3 shared connections)
- [Audit Level Pinning Test](Audit_Level_Pinning_Test.md) (3 shared connections)
- [Payload Redaction Test](Payload_Redaction_Test.md) (3 shared connections)
- [Handler Reconfiguration Test](Handler_Reconfiguration_Test.md) (3 shared connections)
- [Log Append Across Restart Test](Log_Append_Across_Restart_Test.md) (3 shared connections)
- [Console Verbosity Test](Console_Verbosity_Test.md) (3 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (1 shared connections)
- [CLI Shared Plumbing](CLI_Shared_Plumbing.md) (1 shared connections)
- [Logging Test Isolation](Logging_Test_Isolation.md) (1 shared connections)

## Source Files

- `tests/test_logging.py`

## Audit Trail

- EXTRACTED: 176 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*