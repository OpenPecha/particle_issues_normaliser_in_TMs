from pathlib import Path

import requests
from github import Github


class GitHubFileDownloader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_download_url_from_repo_name(self):
        # Create a GitHub instance using your token
        g = Github(self.token)

        # Get the repository
        repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

        # Get the list of contents in the repository root
        contents = repo.get_contents("")

        txt_file_name = ""
        for content_file in contents:
            if content_file.name.endswith(".txt"):
                txt_file_name = content_file.name

        # Get the file contents
        file_contents = repo.get_contents(txt_file_name)
        return file_contents.download_url

    def download_file(self, download_url, destination_folder="."):
        # Send a GET request to download the file
        response = requests.get(download_url)

        new_downloaded_file_name = self.repo_name + ".txt"
        local_file_path = Path(destination_folder) / new_downloaded_file_name
        if response.status_code == 200:
            # Open the local file in binary write mode and save the downloaded content
            with open(local_file_path, "wb") as local_file:
                local_file.write(response.content)
            print(f"File downloaded and saved to {local_file_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")


if __name__ == "__main__":
    # Usage example
    token = "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"
    repo_owner = "MonlamAI"
    repo_name = "BO0791"

    downloader = GitHubFileDownloader(token, repo_owner, repo_name)

    download_url = downloader.get_download_url_from_repo_name()
    downloader.download_file(download_url)
