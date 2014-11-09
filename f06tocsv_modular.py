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


#writes filnames being processed.
def write_filenames(filenames, outpf):
    outpf.writerow(["F06 files", "Time Stamp"])
    for F06 in filenames:
        status = os.path.getmtime(F06)
        date = datetime.datetime.fromtimestamp(status)
        outpf.writerow([F06, str(date)])


#gets keys from a specified key file
def write_and_get_keys(keyfile, outpf):
    KEYS = []
    outpf.writerow(["Keys"])
    outpf.writerow(['Node', 'Element'])
    with open(keyfile) as KEY_FILE:
        for line in KEY_FILE:
            if "Node" not in line:
                values = line[:-1].split(",")
                key = [values[0], values[1]]
                KEYS.append(tuple(key))
                outpf.writerow(key)
        keyset = set(KEYS)
        return keyset


def write_apploads(nextrow, outpf, det, lc, TARGET):
    app_load_raw_pattern = r'^\d?\s+{0}\d+\s+APP'.format(TARGET)
    alc = re.compile(app_load_raw_pattern)
    if alc.search(nextrow):
        d = nextrow.split()
        line = [
            det, lc, int(d[1]), '', d[2], float(d[3]), float(d[4]),
                float(d[5]), float(d[6]), float(d[7]), float(d[8])
        ]
        outpf.writerow(line)


def write_values_that_match_keys(nextrow, outpf, det, lc, ks):
    leading_zero = r'^\d'
    lzc = re.compile(leading_zero)
    if lzc.search(nextrow):
        d = nextrow.split()
        if tuple([d[1], d[2]]) in ks:
            line = [
                det, lc, int(d[1]), int(d[2]), d[3], float(d[4]), float(d[5]),
                float(d[6]), float(d[7]), float(d[8]), float(d[9])
            ]
            outpf.writerow(line)
    else:
        d = nextrow.split()
        if tuple([d[0], d[1]]) in ks:
            line = [
                det, lc, int(d[0]), int(d[1]), d[2], float(d[3]), float(d[4]),
                float(d[5]), float(d[6]), float(d[7]), float(d[8])
            ]
            outpf.writerow(line)


def processf06s(filenames, outputfile, keyset, APPLOAD_TOGGLE, APP_TARGET):
    csv_title = [
        'Detent', 'Loadcase', 'Node', 'Element',
        'Element Type', 'FX', 'FY', 'FZ', 'MX', 'MY', 'MZ'
    ]
    output_file.writerow(csv_title)
    for f06 in filenames:
        next_row = "Initialize to look for pg"
        grid_row = "Initialize to look for grid"
        with open(f06) as F:
            print "Processing {0}".format(f06)
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
                            #this section gets the apploads using a function
                            if APPLOAD_TOGGLE:
                                write_apploads(
                                    next_row, outputfile, detent,
                                    loadcase, APP_TARGET
                                )
                            #this section gets the values attached to the keys
                            #using a function
                            key_pattern = r'^\d?\s+\d+\b\s+\d+\b'
                            kc = re.compile(key_pattern)
                            if kc.search(next_row):
                                write_values_that_match_keys(
                                    next_row, outputfile, detent,
                                    loadcase, keyset
                                )
                            #this finds the end of the section and breaks
                            # to the PAGE & GRID if statement.
                            if "PAGE" in next_row:
                                break
                if ("PAGE" in next_row and
                    "G R I D   P O I N T   F O R C E" in grid_row):
                    title_row = next_row
                else:
                    title_row = F.readline()

if __name__ == '__main__':
    with open('outputmod.csv', 'wb') as O:
        #we want APPLOAD_TOGGLE AND TARGET as a sys.argv in the future
        APPLOADS = True
        TARGET_APPLOADS = 2
        output_file = csv.writer(O, quoting=csv.QUOTE_NONNUMERIC)
        file_names = glob('*.f06')
        write_filenames(file_names, output_file)
        #key_file can be potentially brought in from sys.argv or
        # if no file given then apploads only
        key_file = 'keys.csv'
        key_set = write_and_get_keys(key_file,output_file)
        processf06s(file_names, output_file, key_set, APPLOADS, TARGET_APPLOADS)
    toc = time.clock()
    print toc - tic