# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
    'Under 20':'19',
    '20s': '20',
    '30s': '30',
    '40s': '40',
    '50s': '50',
    '60s': '60',
    '70s': '70',
    'Over 79': '80',
    'Unknown': 'xx'
}

age_group_dict = {
    '0-19':'19',
    '20-29':'20',
    '30-39':'30',
    '40-49':'40',
    '50-59':'50',
    '60-69':'60',
    '70-79':'70',
    '80-89':'80',
    '90+':'80'
}

total_dose1 = 0
vacc_by_age = {}

t0 = date(2020,3,1)
last_date = '2020-03-01'

with open('vaccinated-per-day.csv') as f:

    for j,line in enumerate(f):
        if j == 0:
            header = line.strip().split(',')
            dose1_index = header.index('first_dose')
        else:
            fields = line.strip().split(',')
            data_date = fields[0]
            if data_date > last_date:
                last_date = data_date
            age_text = fields[1]
            age_group = age_group_dict[age_text]

            if data_date not in vacc_by_age:
                vacc_by_age[data_date] = {}
            if age_group not in vacc_by_age[data_date]:
                vacc_by_age[data_date][age_group] = 0
            if fields[dose1_index] != '<15':
                vacc_by_age[data_date][age_group] += int(float(fields[dose1_index]))
                total_dose1 += int(float(fields[dose1_index]))

with open('il-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for group in regional_abbreviations:
        abbrev = regional_abbreviations[group]
        for dat in ['xt']:
            hbuff.append(abbrev + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    cumulative_dose1={}
    for group in regional_abbreviations:
        age_group = regional_abbreviations[group]
        cumulative_dose1[age_group] = 0

    the_date = date(2020, 3, 1)
    date_str = the_date.isoformat()
    done = False
    while date_str <= last_date:
        buff = [date_str]
        for group in regional_abbreviations:
            age_group = regional_abbreviations[group]
            if date_str in vacc_by_age:
                if age_group in vacc_by_age[date_str]:
                    cumulative_dose1[age_group] += vacc_by_age[date_str][age_group]
                    val = cumulative_dose1[age_group]
                    if val > 0:
                        buff.append(str(val))
                    else:
                        buff.append('')
                else:
                    buff.append('')
            else:
                buff.append('')

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
        date_str = the_date.isoformat()

print('Total first doses =',total_dose1)