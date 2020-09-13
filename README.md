# TBP Candidacy Automation
Python script written by PSU's TBP Chapter that aids with TBP candidacy automation.

## Installation
Install Python 3 (if not already installed) then download the two other files from this directory.  

## Instructions for Use
1. Copy the eligibility list from its source to an Excel file and save it as a csv to the same directory as the `python` and `json` (NOTE: if we ever use this for MIT, we'll need to change the `json` file to match our programs) file from this directory.

2. Now, open a terminal and navigate to the directory where the candidacy files are located.

3. Using the terminal, run the python file by typing `python tbpelig.py`.  The program will walk you through running the file.

4. Next, copy the indicated file directly into the eligibility report from the TBP website (you may need to Find and Replace the numerical months and replace them with ‘May’ or ‘Dec’).  The terminal will have invalid major codes listed, then the students from whom they came. The terminal will also have eligible graduate students; these are not reported on the eligibility report, and must be reported vai the graduate student form.
