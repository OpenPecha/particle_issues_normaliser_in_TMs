from pathlib import Path

from src.affix_normaliser.antx_annotation_transfer import antx_annotation_transfer

from .config import TM_FOLDER_DIR


def test_antx_annotation_transfer():
    source_text = (TM_FOLDER_DIR / "TM0791.txt").read_text(encoding="utf-8")
    target_text = (TM_FOLDER_DIR / "TM0791_tokenized_cleaned.txt").read_text(
        encoding="utf-8"
    )

    annotated_text = antx_annotation_transfer(source_text, target_text)
    expected_annotated_text = Path(
        TM_FOLDER_DIR / "TM0791_cleaned_annotated.txt"
    ).read_text(encoding="utf-8")
    assert annotated_text == expected_annotated_text
