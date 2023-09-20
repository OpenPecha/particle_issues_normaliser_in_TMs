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
REPO_OWNER = "MonlamAI"


def filter_bo_repo_names_from_file(file_path) -> List[str]:
    file_content = file_path.read_text(encoding="utf-8")
    BO_PATTERN = r"- ([a-zA-Z\d-]*)"  # Regex to select the bo repo names
    bo_names = re.findall(BO_PATTERN, file_content)
    return bo_names


def get_tm_repo_names_from_bo_names(bo_names: List[str]) -> List[str]:
    bo_ids = [bo_name[2:6] for bo_name in bo_names]
    tm_names = [f"TM{bo_id}" for bo_id in bo_ids]
    return tm_names


def filter_tm_files_by_initial_commit_date_range(
    tm_names: List[str], output_file_path: Path
) -> List[str]:
    tm_names_filtered = []

    # Open the output file for writing
    with open(output_file_path, "w") as output_file:
        for tm_name in tm_names:
            try:
                repo_filter = GitHubRepoFilter(token, REPO_OWNER, tm_name)
                file_names = repo_filter.get_file_names_in_repo()
                bo_txt_file_name = repo_filter.get_bo_txt_file_from_file_names(
                    file_names
                )
                if bo_txt_file_name == "":
                    continue
                initial_commit_date = repo_filter.get_initial_commit_date(
                    bo_txt_file_name
                )
                if (
                    initial_commit_date
                    and START_DATE <= initial_commit_date <= END_DATE
                ):
                    tm_names_filtered.append(tm_name)
                    output_file.write(f"{tm_name}\n")
            except Exception as e:
                print(f"Error processing {tm_name}: {str(e)}")
                continue

    return tm_names_filtered


class GitHubRepoFilter:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_file_names_in_repo(self) -> List[str]:
        g = Github(self.token)
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")
        return repo.get_contents("")

    def get_bo_txt_file_from_file_names(self, file_names: List) -> str:
        target_file_suffix = "bo.txt"
        bo_txt_file_name = ""
        for content_file in file_names:
            if content_file.name.endswith(target_file_suffix):
                bo_txt_file_name = content_file.name
        return bo_txt_file_name

    def get_initial_commit_date(self, file_name):
        g = Github(self.token)
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")
        commits = repo.get_commits(path=file_name)

        if commits:
            commits_count = len(list(commits))
            initial_commit_date = commits[commits_count - 1].commit.author.date
            return initial_commit_date
        else:
            return None


if __name__ == "__main__":
    bo_repos_file_path = Path(PARENT_DIR / DATA_FOLDER_DIR) / "few_BO_EN_list.txt"
    bo_names = filter_bo_repo_names_from_file(bo_repos_file_path)
    tm_names = get_tm_repo_names_from_bo_names(bo_names)

    filtered_tm_output_file_path = (
        Path(PARENT_DIR / DATA_FOLDER_DIR) / "filtered_tm_names.txt"
    )
    tm_names_filtered = filter_tm_files_by_initial_commit_date_range(
        tm_names, filtered_tm_output_file_path
    )
    print(tm_names_filtered)
