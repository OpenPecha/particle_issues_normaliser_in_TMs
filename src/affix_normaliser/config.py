from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
TOP_LEVEL_DIR = PARENT_DIR.parent
DATA_FOLDER_DIR = TOP_LEVEL_DIR / "data"
BO_FOLDER_DIR = DATA_FOLDER_DIR / "BO_files"
TM_FOLDER_DIR = DATA_FOLDER_DIR / "TM_files"
FILTERED_BO_FOLDER_DIR = DATA_FOLDER_DIR / "filtered_BO_files"
FILTERED_TM_FOLDER_DIR = DATA_FOLDER_DIR / "filtered_TM_files"
FILTERED_TOKENIZED_BO_FOLDER_DIR = DATA_FOLDER_DIR / "filtered_tokenized_BO_files"
FILTERED_TOKENIZED_TM_FOLDER_DIR = DATA_FOLDER_DIR / "filtered_tokenized_TM_files"
FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR = (
    DATA_FOLDER_DIR / "filtered_tokenized_cleaned_TM_files"
)
FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR = (
    DATA_FOLDER_DIR / "final_cleaned_annotated_TM_files"
)
ALL_TM_FOLDER_DIR = DATA_FOLDER_DIR / "all_TM_files"

TEST_DIR = DATA_FOLDER_DIR / "test_folder"


AFFIX_ISSUES = [
    "་འི་",
    "་ར་",
    "་ས་",
    "་འམ་",
    "་འང་",
    "་འོ་",
    "་འིའོ་",
    "་འིའམ་",
    "་འིའང་",
    "་འོའམ་",
    "་འོའང་",
    "་འི།",
    "་ར།",
    "་ས།",
    "་འམ།",
    "་འང།",
    "་འོ།",
    "་འིའོ།",
    "་འིའམ།",
    "་འིའང།",
    "་འོའམ།",
    "་འོའང།",
]
