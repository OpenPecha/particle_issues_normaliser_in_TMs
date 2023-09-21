from pathlib import Path
from typing import List, Tuple

from config import AFFIX_ISSUES, FILTERED_TM_FOLDER_DIR


def check_affix_issues(
    text: str, affix_issues: List[str] = AFFIX_ISSUES
) -> Tuple[bool, List[str]]:
    """
    Check if the affix is in the TMs.
    """
    # Check if the affix is in the TMs.
    found_affix_issues = []
    for affix_issue in affix_issues:
        if affix_issue in text:
            found_affix_issues.append(affix_issue)

    if found_affix_issues:
        return True, found_affix_issues
    return False, []


def detect_affix_issues_in_folder(folder_path: Path):
    """
    Detect affix issues in the TMs.
    """
    all_file_content = ""

    txt_files = folder_path.glob("*.txt")

    for txt_file in txt_files:
        file_content = txt_file.read_text(encoding="utf-8")
        all_file_content += file_content

    has_affix_issues, found_affix_issues = check_affix_issues(all_file_content)
    return has_affix_issues, found_affix_issues


if __name__ == "__main__":
    has_affix_issues, found_affix_issues = detect_affix_issues_in_folder(
        FILTERED_TM_FOLDER_DIR
    )
    print(has_affix_issues)
    print(found_affix_issues)
