from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
DATA_FOLDER_DIR = "data"
BO_FOLDER_DIR = PARENT_DIR / DATA_FOLDER_DIR / "BO_files"
TM_FOLDER_DIR = PARENT_DIR / DATA_FOLDER_DIR / "TM_files"
FILTERED_BO_FOLDER_DIR = PARENT_DIR / DATA_FOLDER_DIR / "filtered_BO_files"
FILTERED_TM_FOLDER_DIR = PARENT_DIR / DATA_FOLDER_DIR / "filtered_TM_files"

AFFIX_ISSUES = [
    "་འི",
    "་ར",
    "་ས",
    "་འམ",
    "་འང",
    "་འོ",
    "་འིའོ",
    "་འིའམ",
    "་འིའང",
    "་འོའམ",
    "་འོའང",
]
