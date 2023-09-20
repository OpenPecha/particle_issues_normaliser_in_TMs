import re
from pathlib import Path
from typing import List

from config import DATA_FOLDER_DIR, PARENT_DIR


def filter_bo_repo_names_from_file(file_path) -> List[str]:
    file_content = file_path.read_text(encoding="utf-8")
    BO_PATTERN = r"- ([a-zA-Z\d-]*)"  # Regex to select the bo repo names
    bo_names = re.findall(BO_PATTERN, file_content)
    return bo_names


def get_tm_repo_names_from_bo_names(bo_names: List[str]) -> List[str]:
    bo_ids = [bo_name[2:6] for bo_name in bo_names]
    tm_names = [f"TM{bo_id}" for bo_id in bo_ids]
    return tm_names


if __name__ == "__main__":
    bo_repos_file_path = Path(PARENT_DIR / DATA_FOLDER_DIR) / "all_BO_EN_list.txt"
    bo_names = filter_bo_repo_names_from_file(bo_repos_file_path)
    tm_names = get_tm_repo_names_from_bo_names(bo_names)
    print(tm_names)
