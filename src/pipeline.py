from pathlib import Path

from antx_annotation_transfer import antx_annotation_transfer, remove_newlines
from config import BO_FOLDER_DIR, TM_FOLDER_DIR
from repo_file_downloader import GitHubFileDownloader, download_file_with_url
from repo_file_uploader import GitHubFileUploader
from settings import GITHUB_TOKEN
from tibetan_sentence_tokenizer_pipeline import sentence_tokenizer_pipeline

token = GITHUB_TOKEN


def pipeline(repo_names_list):
    repo_owner = "MonlamAI"

    for bo_repo_name in repo_names_list:

        # downloading bo.txt file
        downloader = GitHubFileDownloader(token, repo_owner, bo_repo_name)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, f"{bo_repo_name}.txt", BO_FOLDER_DIR)

        # downloading TM..-bo.txt file
        translation_memory_ID = bo_repo_name[2:6]
        tm_repo_name = f"TM{translation_memory_ID}"
        downloader = GitHubFileDownloader(token, repo_owner, tm_repo_name)
        download_url = downloader.get_txt_file_download_url_from_repo()
        download_file_with_url(download_url, f"{tm_repo_name}.txt", TM_FOLDER_DIR)

        # sentence tokenizing the bo.txt content
        bo_file_path = BO_FOLDER_DIR / f"{bo_repo_name}.txt"
        bo_file_content = Path(bo_file_path).read_text(encoding="utf-8")
        bo_file_content_tokenized = sentence_tokenizer_pipeline(bo_file_content)
        bo_tokenized_file_name = f"{bo_repo_name}_tokenized.txt"
        tokenized_file_path = BO_FOLDER_DIR / bo_tokenized_file_name
        tokenized_file_path.write_text(bo_file_content_tokenized, encoding="utf-8")

        # transfering the annotation from TM to BO
        source_text = (TM_FOLDER_DIR / f"{tm_repo_name}.txt").read_text(
            encoding="utf-8"
        )
        target_text = bo_file_content_tokenized
        target_text = remove_newlines(target_text)
        AnnotatedText = antx_annotation_transfer(source_text, target_text)
        new_annotated_file_name = f"{tm_repo_name}_cleaned.txt"
        new_annotated_file_path = TM_FOLDER_DIR / new_annotated_file_name
        with open(new_annotated_file_path, "w") as file:
            for AnnotatedLine in AnnotatedText.splitlines():
                file.write(f"{AnnotatedLine.strip()}\n")

        # Uploading the new cleaned file
        repo_owner = "tenzin3"
        repo_name = "test_repo"
        uploader = GitHubFileUploader(token, repo_owner, repo_name)
        file_path = f"TM{translation_memory_ID}-bo.txt"
        file_data = Path(new_annotated_file_path).read_text(encoding="utf-8")
        uploader.upload_txt_file(file_path, file_data)


if __name__ == "__main__":
    repo_names_list = ["BO0790"]
    pipeline(repo_names_list)
