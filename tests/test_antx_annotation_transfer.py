from pathlib import Path

from src.affix_normaliser.antx_annotation_transfer import antx_annotation_transfer


def test_antx_annotation_transfer():
    CURRENT_DIR = Path(__file__).resolve().parent
    DATA_FOLDER_DIR = CURRENT_DIR / "tests_data"
    TM_FOLDER_DIR = DATA_FOLDER_DIR / "TM_files"

    source_text = (TM_FOLDER_DIR / "TM0791.txt").read_text(encoding="utf-8")
    target_text = (TM_FOLDER_DIR / "TM0791_tokenized_cleaned.txt").read_text(
        encoding="utf-8"
    )
    annotated_text = antx_annotation_transfer(source_text, target_text)

    expected_annotated_text = Path(
        TM_FOLDER_DIR / "TM0791_cleaned_annotated.txt"
    ).read_text(encoding="utf-8")
    assert annotated_text == expected_annotated_text
