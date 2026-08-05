"""Text extraction and multi-format loading tests.

Two properties are load-bearing here and each has a test that fails loudly if it
regresses:

* **Extraction does not invent or lose content.** Chunk text is quoted back to a
  user as citation evidence, so a parser that rewrites its input turns that
  evidence into a forgery.
* **One bad file cannot take down a sync.** A corpus is a shared, uncontrolled
  input; the pipeline has to survive the worst file in it.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from osc_assistant.errors import ParseError
from osc_assistant.ingestion import FilesystemLoader, parse
from osc_assistant.ingestion.parsers import SUPPORTED_EXTENSIONS

HTML_SAMPLE = """<!doctype html>
<html><head><title>Access Control Standard</title>
<style>body { color: #333; }</style>
<script>console.log("nav helper");</script>
</head><body>
<h1>Access Control</h1>
<p>Privileged access is granted for a maximum of 8 hours.</p>
<ul><li>Service credentials rotate every 90 days.</li></ul>
</body></html>
"""


def test_supported_extensions_are_lowercase_and_dotted() -> None:
    assert all(ext.startswith(".") and ext.islower() for ext in SUPPORTED_EXTENSIONS)
    assert {".md", ".txt", ".html", ".pdf", ".docx", ".xlsx"} <= set(SUPPORTED_EXTENSIONS)


def test_text_parser_preserves_content_exactly(tmp_path: Path) -> None:
    """The invariant that makes a citation quotable: text in equals text out."""
    body = "# Leave\n\nEmployees accrue 26 days.\n\n- Carry over up to 10 days.\n"
    path = tmp_path / "leave.md"
    path.write_text(body, encoding="utf-8")

    assert parse(path).text == body


def test_html_parser_drops_script_and_style_but_keeps_prose(tmp_path: Path) -> None:
    path = tmp_path / "standard.html"
    path.write_text(HTML_SAMPLE, encoding="utf-8")

    parsed = parse(path)

    assert "8 hours" in parsed.text
    assert "90 days" in parsed.text
    # Script and style bodies are code, and would otherwise be embedded and retrieved.
    assert "console.log" not in parsed.text
    assert "#333" not in parsed.text


def test_html_title_is_taken_from_the_document(tmp_path: Path) -> None:
    """A format that declares its own title beats one derived from the filename."""
    path = tmp_path / "a-file-with-an-unhelpful-name.html"
    path.write_text(HTML_SAMPLE, encoding="utf-8")

    assert parse(path).title == "Access Control Standard"


def test_unsupported_extension_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "archive.zip"
    path.write_bytes(b"PK\x03\x04")

    with pytest.raises(ParseError, match="No parser"):
        parse(path)


def test_corrupt_binary_raises_parse_error_not_a_library_exception(tmp_path: Path) -> None:
    """Callers catch `ParseError`; a raw pypdf exception would escape that."""
    path = tmp_path / "broken.pdf"
    path.write_bytes(b"not a pdf at all")

    with pytest.raises(ParseError):
        parse(path)


def test_docx_extracts_paragraphs_and_table_cells(tmp_path: Path) -> None:
    """Policy documents keep the facts people ask about inside tables."""
    docx = pytest.importorskip("docx")

    path = tmp_path / "handbook.docx"
    document = docx.Document()
    document.add_paragraph("Probation lasts six months.")
    table = document.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Home office allowance"
    table.rows[0].cells[1].text = "600 EUR"
    document.save(str(path))

    parsed = parse(path)

    assert "Probation lasts six months." in parsed.text
    assert "Home office allowance" in parsed.text
    assert "600 EUR" in parsed.text


def test_xlsx_keeps_a_row_together_and_labels_it_with_its_sheet(tmp_path: Path) -> None:
    """A spreadsheet's meaning is two-dimensional; retrieval is not.

    The row is the unit that has to survive, because a scenario workbook's facts —
    a quantity band and the price that applies to it — are only true together.
    """
    openpyxl = pytest.importorskip("openpyxl")

    path = tmp_path / "scenarios.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Tier Pricing"
    sheet.append(["Quantity", "Unit price"])
    sheet.append([500, "$5.76"])
    second = workbook.create_sheet("Notes")
    second.append(["Applies to every size"])
    workbook.save(str(path))

    parsed = parse(path)

    assert "## Tier Pricing" in parsed.text
    assert "## Notes" in parsed.text
    # Cells of one row stay on one line, where an embedding can see them together.
    assert "500\t$5.76" in parsed.text
    assert parsed.metadata["sheet_count"] == 2


def test_empty_xlsx_is_an_error_rather_than_an_unfindable_empty_document(
    tmp_path: Path,
) -> None:
    openpyxl = pytest.importorskip("openpyxl")

    path = tmp_path / "blank.xlsx"
    openpyxl.Workbook().save(str(path))

    with pytest.raises(ParseError, match="no cell values"):
        parse(path)


def test_corrupt_xlsx_raises_parse_error_not_a_library_exception(tmp_path: Path) -> None:
    pytest.importorskip("openpyxl")

    path = tmp_path / "broken.xlsx"
    path.write_bytes(b"not a spreadsheet")

    with pytest.raises(ParseError):
        parse(path)


def test_scanned_pdf_reports_that_it_has_no_text(tmp_path: Path) -> None:
    """A page-image PDF parses cleanly and yields nothing. Indexing an empty
    document silently would make it permanently unfindable, so it is an error."""
    pypdf = pytest.importorskip("pypdf")

    path = tmp_path / "scan.pdf"
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with path.open("wb") as handle:
        writer.write(handle)

    with pytest.raises(ParseError, match="no extractable text"):
        parse(path)


async def test_loader_reads_every_supported_format(tmp_path: Path) -> None:
    (tmp_path / "policy.md").write_text("# Policy\n\nAccrue 26 days.\n", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Incident severity SEV1.\n", encoding="utf-8")
    (tmp_path / "page.html").write_text(HTML_SAMPLE, encoding="utf-8")

    loader = FilesystemLoader(tmp_path)
    documents = [document async for document in loader.load()]

    assert {doc.metadata["extension"] for doc in documents} == {".md", ".txt", ".html"}
    assert all(doc.text for doc in documents)
    assert loader.failures == []


async def test_one_unreadable_file_does_not_abort_the_sync(tmp_path: Path) -> None:
    (tmp_path / "good.md").write_text("# Good\n\nReal content here.\n", encoding="utf-8")
    (tmp_path / "bad.pdf").write_bytes(b"this is not a pdf")

    loader = FilesystemLoader(tmp_path)
    documents = [document async for document in loader.load()]

    assert [doc.title for doc in documents] == ["Good"]
    assert len(loader.failures) == 1
    assert loader.failures[0].source_uri.endswith("bad.pdf")


async def test_failures_are_cleared_in_place_between_runs(tmp_path: Path) -> None:
    """The pipeline is handed this list before iteration and reads it after, so a
    re-run must reuse the same list object rather than rebind it."""
    (tmp_path / "bad.pdf").write_bytes(b"not a pdf")
    loader = FilesystemLoader(tmp_path)
    tracked = loader.failures

    async for _ in loader.load():
        pass
    async for _ in loader.load():
        pass

    assert tracked is loader.failures
    assert len(tracked) == 1, "a second run must not double-count the same failure"


async def test_metadata_records_provenance(tmp_path: Path) -> None:
    """Provenance is denormalised onto every chunk, so it has to be right here."""
    nested = tmp_path / "handbook"
    nested.mkdir()
    (nested / "leave.md").write_text("# Leave\n\nBody.\n", encoding="utf-8")

    documents = [document async for document in FilesystemLoader(tmp_path).load()]

    metadata = documents[0].metadata
    assert metadata["relative_path"] == "handbook/leave.md"
    assert metadata["extension"] == ".md"
    assert metadata["size_bytes"] > 0
    assert documents[0].updated_at is not None


async def test_unsupported_files_are_ignored_not_failed(tmp_path: Path) -> None:
    """A corpus directory holds images and archives. They are not errors."""
    (tmp_path / "diagram.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    with zipfile.ZipFile(tmp_path / "bundle.zip", "w") as archive:
        archive.writestr("x.txt", "x")
    (tmp_path / "real.md").write_text("# Real\n\nContent.\n", encoding="utf-8")

    loader = FilesystemLoader(tmp_path)
    documents = [document async for document in loader.load()]

    assert len(documents) == 1
    assert loader.failures == []
