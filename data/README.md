# About data folder

### all_BO_EN_list.txt

Contains list of all tibetan text corpus (starting iwth BO..) and corresponding english
text corpus (starting with EN...)
The content is copied from the link:

https://github.com/OpenPecha-Data/C1A81F448/blob/main/C1A81F448.opc/meta.yml

and the file is used to get all the list of TM files (this is done by getting the IDs from bo files). such that from file name BO0133, we get ID 0133 and we know there a corresponding TM
file name TM0133.

### all_TM_list.txt

Contains all the TM file names extracted from all_BO_EN_list.txt

### filtered_TMs.txt

Contains TM file names where its initial commit is between 3rd May, 23 and 5th July,23. We have an prior knowledge that affix issues in text happended during that time period

### filtered_error_TMs.txt

Contains TM file names where its initial commit is not between 3rd May,23 and 5th July,23. and one which it doesn't exist(which means there no TM file for corresponding BO file).

### filtered_BO_files filtered_TM_files Folder

Folder to store BO and TM files that are present in the file filtered_TMs.txt

### BO_files TM_files Folder

Folder to store for testing purposese
