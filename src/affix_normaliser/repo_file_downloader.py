from pathlib import Path
from typing import List

import requests
from github import Github
from retrying import retry

from .config import DATA_FOLDER_DIR
from .settings import GITHUB_TOKEN

TOKEN = GITHUB_TOKEN
REPO_OWNER = "MonlamAI"

ERROR_LOG_FILE = "Failed_to_download_TMs.txt"


class GitHubFileDownloader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_txt_file_download_url_from_repo(self):
        # Create a GitHub instance using your token
        g = Github(self.token)

        try:
            # Get the repository
            repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

            # Get the list of contents in the repository root
            contents = repo.get_contents("")

            target_file_suffix = ".txt"
            # TM repo names start with "TM", there would be two .txt files in the repo,
            # one for the Tibetan language and one for the English language
            if self.repo_name.startswith("TM"):
                target_file_suffix = "bo.txt"

            txt_file_name = ""
            for content_file in contents:
                if content_file.name.endswith(target_file_suffix):
                    txt_file_name = content_file.name

            # Get the file contents
            file_contents = repo.get_contents(txt_file_name)
            return file_contents.download_url
        except Exception as error:
            print(f"An error occurred: {error}")
            return None


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

    if download_url is None:
        print("Failed to download file. Download URL is None")
        write_to_error_log(ERROR_LOG_FILE, new_downloaded_file_name)
        return
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
        write_to_error_log(ERROR_LOG_FILE, new_downloaded_file_name)


def download_tm_and_bo_files_from_github(
    tm_files: List[str], tm_output_file_path, bo_output_file_path
):
    tm_files_count = len(tm_files)
    tm_files_counter = 1
    for tm_file in tm_files:

        print(
            f"[{tm_files_counter}/{tm_files_count}] Downloading TM and BO files for {tm_file}"
        )
        tm_files_counter += 1
        # Downloading TM files
        downloader = GitHubFileDownloader(TOKEN, REPO_OWNER, tm_file)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, tm_file + ".txt", tm_output_file_path)

        # Downloading the corresponding BO files
        # bo_file = f"BO{tm_file[2:]}"
        # bo_repo_name = bo_file
        # # For TM file like TM0701-v4,corresponding BO file is BO0701
        # if "-" in bo_file:
        #     bo_repo_name = bo_file[: bo_file.index("-")]
        # downloader = GitHubFileDownloader(TOKEN, REPO_OWNER, bo_repo_name)
        # download_url = downloader.get_txt_file_download_url_from_repo()
        # download_file_with_url(download_url, bo_file + ".txt", bo_output_file_path)


def write_to_error_log(error_log_file, filename):
    # Append the filename to the error log file
    error_log_file_path = DATA_FOLDER_DIR / error_log_file
    with open(error_log_file_path, "a") as log_file:
        log_file.write(f"{filename}: Failed to download: \n")


if __name__ == "__main__":
    # Usage example
    tm_files = Path(DATA_FOLDER_DIR / "all_TMs_list.txt").read_text().split("\n")
    filtered_tm_files_path = Path(DATA_FOLDER_DIR) / "all_TM_files"
    filtered_bo_files_path = Path(DATA_FOLDER_DIR) / "filtered_BO_files"
    tm_files = [element for element in tm_files if element != ""]
    tm_files = tm_files[:3]

    download_tm_and_bo_files_from_github(
        tm_files, filtered_tm_files_path, filtered_bo_files_path
    )

    # repo_name = "BO0790"
    # downloader = GitHubFileDownloader(token, repo_owner, repo_name)
    # download_url = downloader.get_txt_file_download_url_from_repo()
    # download_file_with_url(download_url, repo_name + ".txt", BO_FOLDER_DIR)
