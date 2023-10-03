import shutil
from pathlib import Path

from antx.core import get_diffs

from .affix_cleaner import clean_affix_and_save_in_folder, learn_and_clean_affixes
from .antx_annotation_transfer import (
    annotation_transfer_and_save_in_folder,
    antx_annotation_transfer,
)
from .config import (
    FILTERED_BO_FOLDER_DIR,
    FILTERED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
    TEST_DIR,
)
from .file_utils import convert_tm_file_name_to_bo_file_name
from .settings import GITHUB_TOKEN
from .tibetan_sentence_tokenizer_pipeline import (
    remove_key_caps,
    sentence_tokenizer_pipeline,
    transfer_non_tibetan_chars,
)
from .verify_antx_modification import (
    count_affix_in_string,
    validate_extra_annotation_condition,
    validate_missing_annotation_condition,
)

token = GITHUB_TOKEN


def pipeline():

    # Tokenizing the TM and BO files
    # Only TM files with issues and their corresponding BO files are tokenized
    # sentence_tokenize_and_save_in_folder(
    #     FILTERED_BO_FOLDER_DIR, FILTERED_TOKENIZED_BO_FOLDER_DIR
    # )
    # sentence_tokenize_and_save_in_folder(
    #     FILTERED_TM_FOLDER_DIR, FILTERED_TOKENIZED_TM_FOLDER_DIR
    # )

    # Cleaning the TM files

    clean_affix_and_save_in_folder(
        FILTERED_TOKENIZED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_BO_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    )

    # Annotating the TM files
    annotation_transfer_and_save_in_folder(
        FILTERED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
        FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
    )


def test_tokenize_individual_file(tm_file_name: str):

    tm_file_path = Path(FILTERED_TM_FOLDER_DIR / tm_file_name)
    # Copy the file
    shutil.copy(tm_file_path, TEST_DIR)

    tm_text = tm_file_path.read_text(encoding="utf-8")
    tm_text = remove_key_caps(tm_text)
    tokenized_tm_text = sentence_tokenizer_pipeline(tm_text)
    tokenized_tm_text = transfer_non_tibetan_chars(tm_text, tokenized_tm_text)
    Path(TEST_DIR / f"t_{tm_file_name}").write_text(tokenized_tm_text, encoding="utf-8")

    bo_file_name = convert_tm_file_name_to_bo_file_name(tm_file_name)

    bo_file_path = Path(FILTERED_BO_FOLDER_DIR / bo_file_name)
    # Copy the file
    shutil.copy(bo_file_path, TEST_DIR)

    bo_text = bo_file_path.read_text(encoding="utf-8")
    bo_text = remove_key_caps(bo_text)
    tokenized_bo_text = sentence_tokenizer_pipeline(bo_text)
    tokenized_bo_text = transfer_non_tibetan_chars(bo_text, tokenized_bo_text)
    Path(TEST_DIR / f"t_{bo_file_name}").write_text(tokenized_bo_text, encoding="utf-8")


def test_clean_affixes_individual_file(tm_file_name: str):
    tm_text = Path(TEST_DIR / f"t_{tm_file_name}").read_text(encoding="utf-8")
    bo_file_name = convert_tm_file_name_to_bo_file_name(tm_file_name)
    bo_text = Path(TEST_DIR / f"t_{bo_file_name}").read_text(encoding="utf-8")
    cleaned_tm_text = learn_and_clean_affixes(tm_text, bo_text)
    Path(TEST_DIR / f"c_{tm_file_name}").write_text(cleaned_tm_text, encoding="utf-8")


def test_annotate_individual_file(tm_file_name: str):
    source_text = Path(FILTERED_TM_FOLDER_DIR / tm_file_name).read_text(
        encoding="utf-8"
    )
    target_text = Path(TEST_DIR / f"c_{tm_file_name}").read_text(encoding="utf-8")
    annotated_text = antx_annotation_transfer(source_text, target_text)
    Path(TEST_DIR / f"a_{tm_file_name}").write_text(annotated_text, encoding="utf-8")


def test_individual_file(file_name: str):
    test_tokenize_individual_file(file_name)
    test_clean_affixes_individual_file(file_name)
    test_annotate_individual_file(file_name)
    annotated_file_content = Path(TEST_DIR / f"a_{file_name}").read_text(
        encoding="utf-8"
    )
    original_file_content = Path(TEST_DIR / file_name).read_text(encoding="utf-8")
    differences = list(get_diffs(original_file_content, annotated_file_content))

    (
        has_valid_missing_annotations,
        invalid_missing_annotations,
    ) = validate_missing_annotation_condition(differences)
    (
        has_valid_extra_annotations,
        invalid_extra_annotations,
    ) = validate_extra_annotation_condition(differences)

    if not has_valid_missing_annotations:
        print(invalid_missing_annotations)
    if not has_valid_extra_annotations:
        print(invalid_extra_annotations)

    affix_counts = count_affix_in_string(annotated_file_content)
    print(affix_counts)

    initial_affix_counts = count_affix_in_string(original_file_content)
    print(initial_affix_counts)


if __name__ == "__main__":
    test_individual_file("TM0791.txt")
