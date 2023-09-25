from pathlib import Path

import requests
from github import Github
from retrying import retry

from .affix_check_script import count_files_in_folder
from .config import TM_FOLDER_DIR
from .settings import GITHUB_TOKEN

TOKEN = GITHUB_TOKEN
REPO_OWNER = "tenzin3"


class GitHubFileUploader:
    def __init__(self, token, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token

    def get_file_sha(self, file_path, branch="main"):
        g = Github(self.token)
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")
        try:
            existing_file = repo.get_contents(file_path, ref=branch)
            return existing_file.sha
        except Exception:
            return None  # File doesn't exist, so current SHA is None

    @retry(
        stop_max_attempt_number=3,  # Maximum number of retries
        wait_fixed=2000,  # Delay between retries in milliseconds (2 seconds)
        retry_on_exception=lambda x: isinstance(
            x, requests.exceptions.RequestException
        ),  # Retry on network errors
    )
    def upload_txt_file(self, file_name, file_data):
        g = Github(self.token)
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

        # Get the current SHA hash of the file
        current_sha = self.get_file_sha(file_name)

        # Specify the commit message
        commit_message = "Update file via script"

        if current_sha:
            # File exists, update it
            repo.update_file(
                file_name, commit_message, file_data, current_sha, branch="main"
            )
        else:
            # File doesn't exist, create it
            repo.create_file(file_name, commit_message, file_data, branch="main")


def upload_files_in_folder_to_repo(folder_path: Path):
    txt_files = folder_path.glob("*.txt")
    file_count = count_files_in_folder(folder_path)
    counter = 1

    for txt_file in txt_files:
        print(f"[{counter}/{file_count}]] File {txt_file.name} Uploading...")
        file_content = txt_file.read_text(encoding="utf-8")

        file_name = txt_file.name
        repo_name = txt_file.name
        uploader = GitHubFileUploader(token, repo_owner, repo_name)
        uploader.upload_txt_file(file_name, file_content)
        counter += 1


if __name__ == "__main__":
    # Usage example
    token = GITHUB_TOKEN
    repo_owner = "tenzin3"
    repo_name = "test_repo"

    uploader = GitHubFileUploader(token, repo_owner, repo_name)
    github_repo_file_path = "TM0790-bo.txt"
    file_data = (TM_FOLDER_DIR / "TM0790_cleaned.txt").read_text(encoding="utf-8")
    uploader.upload_txt_file(github_repo_file_path, file_data)
