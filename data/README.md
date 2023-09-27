# About data folder

Some of the folder you might not see because the size was too big and was put in gitignore,
but you understand better with all information available.

## all_BO_EN_list.txt

Contains list of all tibetan text corpus (starting iwth BO..) and corresponding english
text corpus (starting with EN...)
The content is copied from the link:

https://github.com/OpenPecha-Data/C1A81F448/blob/main/C1A81F448.opc/meta.yml

and the file is used to get all the list of TM files (this is done by getting the IDs from bo files). such that from file name BO0133, we get ID 0133 and we know there a corresponding TM
file name TM0133.

## all_TM_list.txt

Contains all the TM file names extracted from all_BO_EN_list.txt
TMs names extracted in all_TMs_list -> 2102

## all_TM_files

Folder containing all the TM files
TM file count = 1998 (2102 - 104)

## Failed_to_download_TMs.txt

List of all TM names that were not able to download. (404)
TMs names not able to download -> 104

## TM_files_with_issues.txt

Using the script affix_check_script in src, there are the list of TM files with possiblity
of affix issues that were able to download from 1998 files.
TM file count = 1553

## TM_files_without_issues.txt

Using the script affix_check_script in src, there are the list of TM files with no
of affix issues that were able to download from 1998 files.
TM file count = 445

Note: 1553 + 445 = 1998

### filtered_BO_files filtered_TM_files Folder

Folder to store BO and TM files that are present in the file filtered_TMs.txt
