import re
from datetime import datetime
from pathlib import Path
from typing import List

from github import Github

from config import DATA_FOLDER_DIR, PARENT_DIR
from settings import GITHUB_TOKEN

token = GITHUB_TOKEN

# These are the dates where TM files were sentence tokenized wrongly
START_DATE = datetime(2023, 5, 3)
END_DATE = datetime(2023, 7, 5)


def filter_bo_repo_names_from_file(file_path) -> List[str]:
    file_content = file_path.read_text(encoding="utf-8")
    BO_PATTERN = r"- ([a-zA-Z\d-]*)"  # Regex to select the bo repo names
    bo_names = re.findall(BO_PATTERN, file_content)
    return bo_names


def get_tm_repo_names_from_bo_names(bo_names: List[str]) -> List[str]:
    bo_ids = [bo_name[2:6] for bo_name in bo_names]
    tm_names = [f"TM{bo_id}" for bo_id in bo_ids]
    return tm_names


class GitHubRepoFilter:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_repositories(self):
        g = Github(self.token)
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")
        return repo.get_contents("")

    def get_bo_txt_file_from_repositories(self, repo_names):
        target_file_suffix = "bo.txt"
        txt_file_name = ""
        for content_file in repo_names:
            if content_file.name.endswith(target_file_suffix):
                txt_file_name = content_file.name
        return txt_file_name


if __name__ == "__main__":
    bo_repos_file_path = Path(PARENT_DIR / DATA_FOLDER_DIR) / "few_BO_EN_list.txt"
    bo_names = filter_bo_repo_names_from_file(bo_repos_file_path)
    tm_names = get_tm_repo_names_from_bo_names(bo_names)

    repo_owner = "MonlamAI"
    repo_name = "TM0701"
    repo_filter = GitHubRepoFilter(token, repo_owner, repo_name)
    repo_names = repo_filter.get_repositories()
    txt_file_name = repo_filter.get_bo_txt_file_from_repositories(repo_names)
    print(txt_file_name)
