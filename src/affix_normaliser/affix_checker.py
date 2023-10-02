from pathlib import Path
from typing import List, Tuple

from .config import AFFIX_ISSUES, ALL_TM_FOLDER_DIR, DATA_FOLDER_DIR
from .file_utils import count_files_in_folder, file_name_without_txt


def check_affix_issues(
    text, affix_issues: List = AFFIX_ISSUES
) -> Tuple[bool, List[str]]:
    # Check if the affix is in the TMs.
    found_affix_issues = []
    for affix_issue in affix_issues:
        if affix_issue in text:
            found_affix_issues.append(affix_issue)

    if found_affix_issues:
        return True, found_affix_issues
    return False, []


def detect_affix_issues_in_folder(folder_path: Path):
    all_file_content = ""

    txt_files = folder_path.glob("*.txt")

    for txt_file in txt_files:
        file_content = txt_file.read_text(encoding="utf-8")
        all_file_content += file_content

    has_affix_issues, found_affix_issues = check_affix_issues(all_file_content)
    return has_affix_issues, found_affix_issues


def identify_files_with_affix_issues(
    folder_path, affix_issues: List[str]
) -> Tuple[List[str], List[str]]:
    txt_files = folder_path.glob("*.txt")
    files_with_issues = []
    files_without_issues = []

    for txt_file in txt_files:
        file_content = txt_file.read_text(encoding="utf-8")
        found_affix = False
        file_name = file_name_without_txt(txt_file.name)
        for issue in affix_issues:
            if issue in file_content:
                files_with_issues.append(file_name)
                found_affix = True
                break
        if not found_affix:
            files_without_issues.append(file_name)

    return files_with_issues, files_without_issues


if __name__ == "__main__":

    files_with_issues, files_without_issues = identify_files_with_affix_issues(
        ALL_TM_FOLDER_DIR, AFFIX_ISSUES
    )

    files_count = count_files_in_folder(ALL_TM_FOLDER_DIR)
    print(f"No of filtered TM files: {files_count}")
    print(f"No of filtered TM files with issues: {len(files_with_issues)}")
    print(f"No of filtered TM files without issues: {len(files_without_issues)}")
    Path(DATA_FOLDER_DIR / "TM_files_with_issues.txt").write_text(
        "\n".join(files_with_issues), encoding="utf-8"
    )
    Path(DATA_FOLDER_DIR / "TM_files_without_issues.txt").write_text(
        "\n".join(files_without_issues), encoding="utf-8"
    )
