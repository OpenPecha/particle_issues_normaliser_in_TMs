from pathlib import Path

from src.affix_normaliser.affix_cleaner import learn_and_clean_affixes

from .config import BO_FOLDER_DIR, TM_FOLDER_DIR


def test_learn_and_clean_affixes():
    test_file_path = TM_FOLDER_DIR / "TM0791_tokenized.txt"
    test_file_content = test_file_path.read_text(encoding="utf-8")

    pattern_file_path = BO_FOLDER_DIR / "BO0791_tokenized.txt"
    pattern_file_content = pattern_file_path.read_text(encoding="utf-8")

    cleaned_content = learn_and_clean_affixes(test_file_content, pattern_file_content)
    expected_cleaned_content = Path(BO_FOLDER_DIR / "BO0791_tokenized.txt").read_text(
        encoding="utf-8"
    )
    assert cleaned_content == expected_cleaned_content
