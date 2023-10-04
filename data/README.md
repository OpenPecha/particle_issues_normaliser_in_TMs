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

## filtered_BO_files

bo files downloaded from TM_files_with_issues.txt
No of BO files downloaded: 1443

## Failed_to_download_BOs.txt

List of all BO names that were not able to download. (404)
TMs names not able to download -> 107

Note: 1443 + 107 = 1550 , but no of TM_with_issues = 1553
Three Ids missing are '0714-v1', '0701-v4', '0718-v2'.
This happened becauses both TM0714-v1 and TM0714 are segmented from same bo file BO0714.
Like wise for  TM0701-v4 and TM0701 are segmented from BO0701.

## filtered_TM_files Folder

Folder to TM files with issues.

## antx_annotation_transfer_log.txt

List of TM names that were annotated correctly.

## antx_annotattion_transfer_error_log.txt

List of TM names that had i. Extra annotations ii. Missing annotations comparing with the initial downloaded tm file. It also contains names of the name that were not changed in this whole cleaning and annotation process.

## affix_counts_in_TMs.tsv

Contains Tm with their affix counts in list. first element contains the affix name, affix count of the cleaned file, then afffix count initially.
TM0781-bo.txt    ['་འི་: ', '0     ', '480   '] ['་ར་: ', '26    ', '212   '].

## affix_reduced_file_names.txt

List of TM file names where its affix is reduced after this cleaning and annotation process.
Count = 757 files. (file that will be upload.)

## affix_reduced_file_but_with_error.txt

Contain TM name with their errors if their affix is reduced. Errors occured due to the presence of
tibetan grammatical errors or absolute exceptions (which were cleaned by 'bo_sent_tokenizer' from mt-tools).

Example: བོད་ཀྱི་མཁས་པ་ཁ་ཅིག སྟོན་པ། (no tsek after ག), སྤྱིར་བཏང་ནང་ལ་གནས་ཚུལ་ཨུམ་ཨུམ་་་། (multiple tsek before shad)
