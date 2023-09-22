from pathlib import Path

from src.affix_normaliser.tibetan_sentence_tokenizer_pipeline import (
    sentence_tokenizer_pipeline,
)

from .config import BO_FOLDER_DIR


def test_tibetan_sentence_tokenizer_pipeline():
    test_file_path = BO_FOLDER_DIR / "BO0791.txt"
    test_file_content = test_file_path.read_text(encoding="utf-8")
    tokenized_content = sentence_tokenizer_pipeline(test_file_content)

    expected_tokenized_content = Path(BO_FOLDER_DIR / "BO0791_tokenized.txt").read_text(
        encoding="utf-8"
    )
    assert tokenized_content == expected_tokenized_content
