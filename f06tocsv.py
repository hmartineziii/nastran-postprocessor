#!/usr/bin/python
# (c)Hector Martinez III
#This code is for the purpose of GRID POINT FORCE load extraction for the 737 MAX Trailing Edge Team,
#applicability is very narrow. Use it while acknowledging ownership of errors or mistakes due to
#misuse of this code.

from glob import glob
import csv
import re
import time
import os
import datetime

tic = time.clock()
APPLOAD_TOGGLE = True
TARGET = 2
KEYS = []

#---------APP-LOAD REGEX SECTION--------------------------
app_load_raw_pattern = r'^\d?\s+{0}\d+\s+APP'.format(TARGET)
alc = re.compile(app_load_raw_pattern)
#------------------------------------------------



next_row = "Initialize to look for pg"
grid_row = "Initialize to look for grid"

with open('output.csv', 'wb') as O:
    output_file = csv.writer(O, quoting=csv.QUOTE_NONNUMERIC)
    file_names = glob('*.f06')
    output_file.writerow(["F06 files","Time Stamp"])
    for f06 in file_names:
        status = os.path.getmtime(f06)
        date = datetime.datetime.fromtimestamp(status)
        print str(date)
        output_file.writerow([f06,str(date)])
    output_file.writerow(["Keys"])
    output_file.writerow(['Node','Element'])
    with open('keys.csv') as KEY_FILE:
        for line in KEY_FILE:
            if "Node" not in line:
                values = line[:-1].split(",")
                key=[values[0],values[1]]
                KEYS.append(tuple(key))
                output_file.writerow(key)
        key_set = set(KEYS)
    csv_title = ['Detent','Loadcase','Node','Element','Element Type','FX','FY','FZ','MX','MY','MZ']
    output_file.writerow(csv_title)
    for file in file_names:
        with open(file) as F:
            print "Processing {0}".format(file)
            title_row = F.readline()
            while True:
                if "END OF JOB" in title_row:
                    break
                if "PAGE" in title_row:
                    detent_row = F.readline()
                    load_case_row = F.readline()
                    blank_row = F.readline()
                    grid_row = F.readline()
                    if "G R I D   P O I N T   F O R C E" in grid_row:
                        detent = detent_row.split()[1]
                        loadcase = load_case_row.split()[1]
                        while True:
                            next_row = F.readline()
                            if APPLOAD_TOGGLE:
                                if alc.search(next_row):
                                    d = next_row.split()
                                    line = [
                                        detent, loadcase, d[1],'',d[2], d[3], d[4],
                                        d[5], d[6], d[7], d[8]
                                    ]
                                    output_file.writerow(line)
                            key_pattern= r'^\d?\s+\d+\b\s+\d+\b'
                            kc=re.compile(key_pattern)
                            if kc.search(next_row):
                                leading_zero= r'^\d'
                                lzc=re.compile(leading_zero)
                                if lzc.search(next_row):
                                    d = next_row.split()
                                    if tuple([d[1],d[2]]) in key_set:
                                        line = [
                                        detent, loadcase, d[1], d[2], d[3], d[4], d[5],
                                        d[6], d[7], d[8], d[9]
                                        ]
                                        output_file.writerow(line)
                                else:
                                    d = next_row.split()
                                    if tuple([d[0],d[1]]) in key_set:
                                        line = [
                                        detent, loadcase, d[0], d[1], d[2], d[3], d[4],
                                        d[5], d[6], d[7], d[8]
                                        ]
                                        output_file.writerow(line)
                            if "PAGE" in next_row:
                                break
                if ("PAGE" in next_row and
                        "G R I D   P O I N T   F O R C E" in grid_row):
                    title_row = next_row
                else:
                    title_row = F.readline()
toc = time.clock()
print toc - tic