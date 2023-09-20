from pathlib import Path

import requests
from github import Github
from retrying import retry

from config import BO_FOLDER_DIR
from settings import GITHUB_TOKEN


class GitHubFileDownloader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_txt_file_download_url_from_repo(self):
        # Create a GitHub instance using your token
        g = Github(self.token)

        # Get the repository
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

        # Get the list of contents in the repository root
        contents = repo.get_contents("")

        target_file_suffix = ".txt"
        # TM repo names start with "TM", there would two .txt files in the repo,
        # one for the tibetan language and one for the english language
        if self.repo_name.startswith("TM"):
            target_file_suffix = "bo.txt"

        txt_file_name = ""
        for content_file in contents:
            if content_file.name.endswith(target_file_suffix):
                txt_file_name = content_file.name

        # Get the file contents
        file_contents = repo.get_contents(txt_file_name)
        return file_contents.download_url


@retry(
    stop_max_attempt_number=3,  # Maximum number of retries
    wait_fixed=2000,  # Delay between retries in milliseconds (2 seconds)
    retry_on_exception=lambda x: isinstance(
        x, requests.exceptions.RequestException
    ),  # Retry on network errors
)
def download_file_with_url(
    download_url, new_downloaded_file_name, destination_folder="."
):
    # Send a GET request to download the file
    response = requests.get(download_url)

    new_downloaded_file_name = new_downloaded_file_name
    local_file_path = Path(destination_folder) / new_downloaded_file_name
    if response.status_code == 200:
        # Open the local file and save the downloaded content
        with open(local_file_path, "wb") as local_file:
            local_file.write(response.content)
        print(f"File downloaded and saved to {local_file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


if __name__ == "__main__":
    # Usage example
    token = GITHUB_TOKEN
    repo_owner = "MonlamAI"
    repo_name = "BO0790"

    downloader = GitHubFileDownloader(token, repo_owner, repo_name)
    download_url = downloader.get_txt_file_download_url_from_repo()
    download_file_with_url(download_url, repo_name + ".txt", BO_FOLDER_DIR)
