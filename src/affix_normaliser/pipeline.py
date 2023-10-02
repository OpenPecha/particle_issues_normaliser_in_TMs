import shutil
from pathlib import Path

from antx.core import get_diffs

from .affix_cleaner import (
    clean_affix_and_save_in_folder,
    file_name_without_txt,
    learn_and_clean_affixes,
    remove_version_number_from_file_name,
)
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
from .settings import GITHUB_TOKEN
from .tibetan_sentence_tokenizer_pipeline import (
    remove_key_caps,
    sentence_tokenizer_pipeline,
    transfer_non_tibetan_chars,
)
from .verify_antx_modification import (
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
    Path(TEST_DIR / f"t_{tm_file_name}").write_text(tokenized_tm_text)

    tm_repo_name = file_name_without_txt(tm_file_name)
    bo_repo_name = f"BO{tm_repo_name[2:]}"
    bo_repo_name = remove_version_number_from_file_name(bo_repo_name)
    bo_file_name = f"{bo_repo_name}.txt"

    bo_file_path = Path(FILTERED_BO_FOLDER_DIR / bo_file_name)
    # Copy the file
    shutil.copy(bo_file_path, TEST_DIR)

    bo_text = bo_file_path.read_text(encoding="utf-8")
    bo_text = remove_key_caps(bo_text)
    tokenized_bo_text = sentence_tokenizer_pipeline(bo_text)
    tokenized_bo_text = transfer_non_tibetan_chars(bo_text, tokenized_bo_text)
    Path(TEST_DIR / f"t_{bo_file_name}").write_text(tokenized_bo_text)


def test_clean_affixes_individual_file(tm_file_name: str):
    tm_text = Path(TEST_DIR / f"t_{tm_file_name}").read_text(encoding="utf-8")

    tm_repo_name = file_name_without_txt(tm_file_name)
    bo_repo_name = f"BO{tm_repo_name[2:]}"
    bo_repo_name = remove_version_number_from_file_name(bo_repo_name)
    bo_file_name = f"{bo_repo_name}.txt"

    bo_text = Path(TEST_DIR / f"t_{bo_file_name}").read_text(encoding="utf-8")
    cleaned_tm_text = learn_and_clean_affixes(tm_text, bo_text)
    Path(TEST_DIR / f"c_{tm_file_name}").write_text(cleaned_tm_text)


def test_annotate_individual_file(tm_file_name: str):
    source_text = Path(FILTERED_TM_FOLDER_DIR / tm_file_name).read_text(
        encoding="utf-8"
    )
    target_text = Path(TEST_DIR / f"c_{tm_file_name}").read_text(encoding="utf-8")
    annotated_text = antx_annotation_transfer(source_text, target_text)
    Path(TEST_DIR / f"a_{tm_file_name}").write_text(annotated_text)


def test_individual_file(file_name: str):
    # test_tokenize_individual_file(file_name)
    # test_clean_affixes_individual_file(file_name)
    # test_annotate_individual_file(file_name)
    differences = list(
        get_diffs(
            Path(FILTERED_TM_FOLDER_DIR / file_name).read_text(encoding="utf-8"),
            Path(TEST_DIR / f"a_{file_name}").read_text(encoding="utf-8"),
        )
    )
    (
        has_valid_missing_annotations,
        unvalid_missing_annotations,
    ) = validate_missing_annotation_condition(differences)
    (
        has_valid_extra_annotations,
        unvalid_extra_annotations,
    ) = validate_extra_annotation_condition(differences)

    if not has_valid_missing_annotations:
        print(unvalid_missing_annotations)
    if not has_valid_extra_annotations:
        print(unvalid_extra_annotations)


if __name__ == "__main__":
    test_individual_file("TM2971.txt")
