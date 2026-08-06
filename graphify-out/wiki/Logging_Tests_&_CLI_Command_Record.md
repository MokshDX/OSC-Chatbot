# Logging Tests & CLI Command Record

> 61 nodes · cohesion 0.07

## Key Concepts

- **test_logging.py** (40 connections) — `tests/test_logging.py`
- **Path** (36 connections)
- **_records()** (30 connections) — `tests/test_logging.py`
- **log_command()** (6 connections) — `src/osc_assistant/cli/_shared.py`
- **test_positional_arguments_are_payload_and_stay_out_by_default()** (5 connections) — `tests/test_logging.py`
- **test_the_command_that_ran_is_named_in_the_log()** (5 connections) — `tests/test_logging.py`
- **test_token_counts_are_not_mistaken_for_credentials()** (5 connections) — `tests/test_logging.py`
- **test_an_unserialisable_value_does_not_lose_the_record()** (4 connections) — `tests/test_logging.py`
- **test_audit_survives_a_coarser_operational_level()** (4 connections) — `tests/test_logging.py`
- **test_credential_fields_are_redacted()** (4 connections) — `tests/test_logging.py`
- **test_credentials_are_redacted_even_with_payload_capture_on()** (4 connections) — `tests/test_logging.py`
- **test_each_pipeline_stage_logs_once_at_trace_level()** (4 connections) — `tests/test_logging.py`
- **test_every_record_inside_a_trace_carries_its_trace_id()** (4 connections) — `tests/test_logging.py`
- **test_payload_capture_records_the_whole_invocation()** (4 connections) — `tests/test_logging.py`
- **test_reconfiguring_does_not_duplicate_records()** (4 connections) — `tests/test_logging.py`
- **test_records_are_appended_across_reconfiguration()** (4 connections) — `tests/test_logging.py`
- **test_the_console_can_be_quieter_than_the_file()** (4 connections) — `tests/test_logging.py`
- **test_third_party_debug_output_is_pinned_out_of_our_stream()** (4 connections) — `tests/test_logging.py`
- **_restore_logging()** (3 connections) — `tests/test_logging.py`
- **test_a_failing_stage_still_logs_its_span_with_the_error()** (3 connections) — `tests/test_logging.py`
- **test_a_log_file_is_created_and_records_land_in_it()** (3 connections) — `tests/test_logging.py`
- **test_an_exception_is_recorded_with_its_traceback()** (3 connections) — `tests/test_logging.py`
- **test_an_explicit_trace_id_on_the_call_site_is_not_overwritten()** (3 connections) — `tests/test_logging.py`
- **test_an_unwritable_log_directory_does_not_stop_the_process()** (3 connections) — `tests/test_logging.py`
- **test_audit_records_go_to_their_own_file()** (3 connections) — `tests/test_logging.py`
- *... and 36 more nodes in this community*

## Relationships

- [Evaluation CLI Command](Evaluation_CLI_Command.md) (2 shared connections)
- [Diagnostic CLI Commands](Diagnostic_CLI_Commands.md) (1 shared connections)
- [Logging Subsystem Core](Logging_Subsystem_Core.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/_shared.py`
- `tests/test_logging.py`

## Audit Trail

- EXTRACTED: 254 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*