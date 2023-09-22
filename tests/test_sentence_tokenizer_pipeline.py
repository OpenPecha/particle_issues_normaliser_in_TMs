from pathlib import Path

from src.tibetan_sentence_tokenizer_pipeline import sentence_tokenizer_pipeline


def test_tibetan_sentence_tokenizer_pipeline():
    CURRENT_DIR = Path(__file__).resolve().parent
    DATA_FOLDER_DIR = CURRENT_DIR / "data"
    BO_FOLDER_DIR = DATA_FOLDER_DIR / "BO_files"

    test_file_path = BO_FOLDER_DIR / "BO0791.txt"
    test_file_content = test_file_path.read_text(encoding="utf-8")
    tokenized_content = sentence_tokenizer_pipeline(test_file_content)

    expected_tokenized_content = Path(
        DATA_FOLDER_DIR / "BO0791_tokenized.txt"
    ).read_text(encoding="utf-8")
    assert tokenized_content == expected_tokenized_content
