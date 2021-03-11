## The purpose of this project is as follows:
This project automatically updates CUNYfirst Human Capital Management Job Data with spreadsheet data from SOTA Systems PR-Assist. 
## Here's some back story on why I needed to build this:
Updating Job Data is laborious, repetitive, simple, and necessary. It is susceptible to pitfalls such as inattentiveness, lack of available time, and low skill threshold. This is an ideal process to automate and free up humans to do higher order work.
## This project leverages the following libraries:
numpy, pandas, fuzzywuzzy, selenium, webdriver_manager, xlrd
## In order to use this, you'll first need do the following:
The user will need to have USERNAME and PASSWORD for CUNYfirst stored as vars, whether running from commandline or in an IDE. If the user does not add a download directory to the main call, like main(USERNAME,PASSWORD,download_dir=X:\\somedir), they will need to modify the code in the main function to reflect the desired default directory. User must, obviously, have both a valid CUNYfirst account and EDIT access to HCM. In order to use the main function, user must have access to PR-Assist OR must have a datastream with similar input data (emplid, record, effective date, end date, action, reason, hours, etc). 
## The expected frequency for running this code is as follows:
Daily