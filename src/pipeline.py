from config import github_token_access
from repo_file_downloader import GitHubFileDownloader, download_file_with_url


def pipeline(repo_names_list):
    repo_owner = "MonlamAI"

    for bo_repo_name in repo_names_list:
        token = github_token_access
        downloader = GitHubFileDownloader(token, repo_owner, bo_repo_name)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, bo_repo_name + ".txt")

        # TM
        translation_memory_ID = bo_repo_name[2:6]
        tm_repo_name = f"TM{translation_memory_ID}"
        downloader = GitHubFileDownloader(token, repo_owner, tm_repo_name)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, tm_repo_name + ".txt")


if __name__ == "__main__":
    repo_names_list = ["BO0791"]
    pipeline(repo_names_list)
