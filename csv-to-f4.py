# Python 3.7.
''' 
Python script for transforming my time report
into a specific format required by HR Department.
''' 

import csv
import datetime
import sys
import time

CSV_FILE = sys.argv[1] #'report.csv'
REPORT_OUTPUT = sys.argv[2] #'out.csv' 

STAGES = {
    None: '',
    'E_ANA': '0005',
    'E_TEST': '0007',
    'E_CODE': '0006',
    'E_MEET': '0106'
}

with_folio = []
without_folio = []

def get_duration(time_str):
    t = time.strptime(time_str, '%H:%M:%S')
    delta_min = 1 if t.tm_min >=40 else 0.5
    duration = t.tm_hour + delta_min
    return duration

def get_folio(tags=[]):
    for t in tags:
        if 'F_' in t:
            return t
    return None

def get_stage(tags=[]):
    for t in tags:
        if 'E_' in t:
            return t
    return None

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

# Read the file from csv
# Format: Project, Client, Title, Duration
with open(CSV_FILE, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        tags = (row['Tags']).split(',')
        folio = get_folio(tags)
        stage = get_stage(tags)
        stage = STAGES[None if stage is None else stage.strip()]
        duration = get_duration(row['Duration'])
        if folio is not None:
            folio = folio.split('F_')[1]
            with_folio.append([
                '',
                row['Project'],
                '',
                folio,
                stage,
                row['Description'],
                duration
            ])
        else:
            without_folio.append([
                row['Project'],
                '',
                stage,
                row['Description'],
                duration
            ])

print(with_folio)
print (without_folio)

# Write to File
with open(REPORT_OUTPUT, 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(with_folio)
    writer.writerows([])
    writer.writerows([])
    writer.writerows(without_folio)