import shutil
from pathlib import Path
from typing import List

from affix_normaliser.config import (
    ALL_TM_FOLDER_DIR,
    DATA_FOLDER_DIR,
    FILTERED_BO_FOLDER_DIR,
)


def filter_empty_elements_from_list(input_list: List[str]) -> List[str]:
    input_list = list(filter(None, input_list))
    return input_list


def extract_content_from_file(file_path: Path) -> List[str]:
    extracted_content = Path(file_path).read_text(encoding="utf-8").split("\n")
    extracted_content = filter_empty_elements_from_list(extracted_content)
    extracted_content = [
        file_name_without_txt(file_name) for file_name in extracted_content
    ]
    return extracted_content


def get_file_names_in_folder(folder_path: Path) -> List[str]:
    file_names = []
    folder_path = Path(folder_path)

    for file_path in folder_path.iterdir():
        if file_path.is_file():
            f_name = file_name_without_txt(file_path.name)
            file_names.append(f_name)

    return file_names


def file_name_without_txt(file_name: str) -> str:
    index = file_name.find(".txt")
    if index != -1:
        return file_name[:index]
    return file_name


def remove_duplicates(input_list: List) -> List:
    return list(set(input_list))


def list_difference(list1, list2):
    return [item for item in list1 if item not in list2]


def count_files_in_folder(folder_path: Path) -> int:
    return len([item for item in folder_path.iterdir() if item.is_file()])


def remove_version_number_from_file_name(file_name: str) -> str:
    index = file_name.find("-v")
    if index != -1:
        return file_name[:index]
    return file_name


def convert_tm_file_name_to_bo_file_name(tm_file_name: str) -> str:
    tm_repo_name = file_name_without_txt(tm_file_name)
    bo_repo_name = f"BO{tm_repo_name[2:]}"
    bo_repo_name = remove_version_number_from_file_name(bo_repo_name)
    bo_file_name = f"{bo_repo_name}.txt"
    return bo_file_name


def copy_files(file_list: List[str], source_folder: Path, destination_folder: Path):
    try:
        source_path = Path(source_folder)
        destination_path = Path(destination_folder)

        # Check if the source folder exists
        if not source_path.exists():
            raise FileNotFoundError(f"Source folder '{source_path}' does not exist.")

        # Create the destination folder if it doesn't exist
        destination_path.mkdir(parents=True, exist_ok=True)

        for file_name in file_list:
            source_file = source_path / file_name
            destination_file = destination_path / file_name

            # Check if the file exists in the source folder
            if not source_file.exists():
                print(f"File '{file_name}' does not exist in the source folder.")
                continue

            # Copy the file to the destination folder
            shutil.copy(source_file, destination_file)
            print(f"File '{file_name}' copied successfully to the destination folder.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":

    tm_downloaded = get_file_names_in_folder(ALL_TM_FOLDER_DIR)
    tm_downloaded_count = len(tm_downloaded)

    tm_with_issues = extract_content_from_file(
        DATA_FOLDER_DIR / "TM_files_with_issues.txt"
    )
    tm_with_issues_count = len(tm_with_issues)

    bo_downloaded = get_file_names_in_folder(FILTERED_BO_FOLDER_DIR)
    bo_downloaded_count = len(bo_downloaded)

    bo_failed_download = extract_content_from_file(
        DATA_FOLDER_DIR / "Failed_to_download_BOs.txt"
    )
    bo_failed_count = len(bo_failed_download)

    bo_files = bo_downloaded + bo_failed_download

    print(f"No of TM files downloaded: {tm_downloaded_count}")
    print(f"No of TM files with issues: {tm_with_issues_count}")
    print(f"No of BO files downloaded: {bo_downloaded_count}")
    print(f"No of BO files failed to download: {bo_failed_count}")
    print(
        f"No of BO file missing: {tm_with_issues_count - bo_downloaded_count - bo_failed_count}"
    )

    tm_with_issues = remove_duplicates(tm_with_issues)
    unique_tm_ids = [tm_issue[2:] for tm_issue in tm_with_issues]

    bo_files = remove_duplicates(bo_files)
    unique_bo_ids = [bo_file[2:] for bo_file in bo_files]

    print(f"No of unique TM ids: {len(unique_tm_ids)}")
    print(f"No of unique BO ids: {len(unique_bo_ids)}")

    print(
        f"Unique TM ids not in BO ids: {list_difference(unique_tm_ids, unique_bo_ids)}"
    )
