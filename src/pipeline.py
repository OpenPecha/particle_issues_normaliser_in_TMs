from pathlib import Path

from bo_sentence_tokenizer_pipeline import bo_sent_tokenizer_pipeline
from config import github_token_access
from repo_file_downloader import GitHubFileDownloader, download_file_with_url


def pipeline(repo_names_list):
    repo_owner = "MonlamAI"

    for bo_repo_name in repo_names_list:
        token = github_token_access

        # downloading bo.txt file
        downloader = GitHubFileDownloader(token, repo_owner, bo_repo_name)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, bo_repo_name + ".txt")

        # downloading TM..-bo.txt file
        translation_memory_ID = bo_repo_name[2:6]
        tm_repo_name = f"TM{translation_memory_ID}"
        downloader = GitHubFileDownloader(token, repo_owner, tm_repo_name)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, tm_repo_name + ".txt")

        # setence tokenizing the bo.txt content
        bo_file_path = f"{bo_repo_name}.txt"
        bo_file_content = Path(bo_file_path).read_text(encoding="utf-8")
        bo_file_content_segmented = bo_sent_tokenizer_pipeline(bo_file_content)
        bo_segmented_file_path = f"{bo_repo_name}_segmented.txt"
        with open(bo_segmented_file_path, "w", encoding="utf-8") as file:
            file.write(bo_file_content_segmented)


if __name__ == "__main__":
    repo_names_list = ["BO0790"]
    pipeline(repo_names_list)
