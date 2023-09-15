import base64

import requests

from config import github_token_access


class GitHubFileUploader:
    def __init__(self, token, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token

    def get_file_sha(self, file_path, branch="main"):
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}?ref={branch}"
        response = requests.get(url, headers={"Authorization": f"token {self.token}"})
        if response.status_code == 200:
            return response.json()["sha"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.json()}")

    def upload_txt_file(self, file_path, branch="main"):
        sha = self.get_file_sha(file_path, branch)
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
        content = open(file_path).read()
        encoded_content = base64.b64encode(
            content.encode()
        ).decode()  # Encode content to base64
        response = requests.put(
            url,
            json={
                "message": "Update file via script",
                "content": encoded_content,
                "sha": sha,
                "branch": branch,
            },
            headers={
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        if response.status_code == 200:
            print(f'File "{file_path}" updated successfully!')
        else:
            print(f"Error: {response.status_code} - {response.json()}")


if __name__ == "__main__":
    # Usage example
    token = github_token_access
    repo_owner = "tenzin3"
    repo_name = "test_repo"

    uploader = GitHubFileUploader(token, repo_owner, repo_name)
    uploader.upload_txt_file("new_TM0790.txt")
