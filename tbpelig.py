#!/usr/bin/env python3
#Author: David S. McDermott
#To run this on a Mac, use Notepad++ to change the line endings from Windows(CR LF) to Mac(CR)
import json
import csv
from datetime import datetime
import re

semesterregex = re.compile(r"(\d+).*")
currentmonth = int(datetime.now().strftime('%m'))
currentyear = int(datetime.now().strftime('%Y'))
currentseason = 'Spring' if currentmonth < 7 else 'Fall'

print("Welcome to the TBP Eligibililty report generator by chapter PA Beta")
print("Please copy your elibible candidates into a list with the following format")
print("A CSV file with no header and columns the order: first name, last name, PSU email, grad term (or blank), PSU major(s), semester standing")
print("Extra columns beyond this will be ignored, and rows with empty cells in one of the rows listed will be ignored")

fname = input("Please enter the name of the file containing your eligible candidates: ")

with open('majormap.json') as f:
    majormap = json.load(f)

candidates = []
invalidcandidates = []
graduatecandidates = []

print("The program will now attempt to read your candidates")
with open(fname) as f:
    csvreader = csv.reader(f, delimiter=',', quotechar='"')
    print("The candidate file has been loaded; please look out for invalid data")
    print("Invalid majors may be caused by dual majors, new engineering majors, or invalid students")
    for row in csvreader:
        if row[0] is None or row[0] == '':
            continue
        candidate = {'firstname':row[1], 'lastname':row[0], 'email':row[2]}
        majors = [entry.strip() for entry in row[4].split(',')]
        for major in majors:
            try:
                candidate['major'] = majormap[major]
                break
            except KeyError:
                print("Invalid major:", major)
        if 'major' not in candidate.keys():
            candidate['rejected'] = 'INVALID_MAJOR: '+str(majors)
            invalidcandidates.append(candidate)
            continue
        match = semesterregex.match(row[5])
        if match:
            semester = int(match[1])
            if semester < 6:
                candidate['standing'] = 'Junior'
                candidate['gradmonth'] = '12' if currentseason == 'Spring' else '5'
                candidate['gradyear'] = currentyear+1 if currentseason == 'Spring' else currentyear+2
            elif semester == 6:
                candidate['standing'] = 'Junior'
                candidate['gradyear'] = currentyear+1
                candidate['gradmonth'] = '5' if currentseason == 'Spring' else '12'
            elif semester == 7:
                candidate['standing'] = 'Senior'
                candidate['gradmonth'] = '5' if currentseason == 'Spring' else '12'
                candidate['gradyear'] = currentyear if currentseason == 'Spring' else currentyear+1
            elif semester > 7:
                candidate['standing'] = 'Senior'
                candidate['gradyear'] = currentyear
                candidate['gradmonth'] = '5' if currentseason == 'Spring' else '12'
            candidates.append(candidate)
        else:
            candidate['graduate'] = row[5]
            graduatecandidates.append(candidate)
            
print()
print("Invalid candidates:")
for candidate in invalidcandidates:
    print(candidate)

print()
print("Graduate candidates:")
for candidate in graduatecandidates:
    print(candidate)

print()
candidates.sort(key=lambda item: (item['standing'], item['lastname'], item['firstname']))
with open(fname[:-4]+"_ugrad.csv", 'w') as f:
    for candidate in candidates:
        print(candidate['firstname']+ ','+ ','+ candidate['lastname']+ ','+ candidate['standing']+ ','+ str(candidate['gradmonth'])+','+str(candidate['gradyear'])+','+candidate['major']+','+ ' '+ ','+ candidate['email'], file=f)
print("Please copy the members from", fname[:-4]+"_ugrad.csv", "to your eligibility report")