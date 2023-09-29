from .affix_cleaner import clean_affix_and_save_in_folder
from .antx_annotation_transfer import annotation_transfer_and_save_in_folder
from .config import (
    FILTERED_BO_FOLDER_DIR,
    FILTERED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
)
from .settings import GITHUB_TOKEN
from .tibetan_sentence_tokenizer_pipeline import sentence_tokenize_and_save_in_folder

token = GITHUB_TOKEN


def pipeline():

    # Tokenizing the TM and BO files
    # Only TM files with issues and their corresponding BO files are tokenized
    sentence_tokenize_and_save_in_folder(
        FILTERED_BO_FOLDER_DIR, FILTERED_TOKENIZED_BO_FOLDER_DIR
    )
    sentence_tokenize_and_save_in_folder(
        FILTERED_TM_FOLDER_DIR, FILTERED_TOKENIZED_TM_FOLDER_DIR
    )

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


if __name__ == "__main__":
    pipeline()
