# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
    'East Midlands':'EM',
    'East of England':'EE',
    'London':'LN',
    'North East':'NE',
    'North West':'NW',
    'South East':'SE',
    'South West':'SW',
    'West Midlands':'WM',
    'Yorkshire and Humber':'YH',
    'England':'EN'
}

total_cases = 0
total_variants = 0
weekly_cases_by_region = {}
weekly_variants_by_region = {}
t0 = date(2020,3,1)
last_week = '2020-03-01'

with open('uk_var.csv') as f:

    for j,line in enumerate(f):
        if j == 0:
            header = line.strip().split(',')
            cases_index = header.index('n_Total')
            variants_index = header.index('n_Confirmed SGTF')
        else:
            fields = line.strip().split(',')
            data_week_text = fields[1].split('-')
            data_week = '-'.join(list(reversed(data_week_text)))

            region = fields[0]
            if data_week not in weekly_cases_by_region:
                weekly_cases_by_region[data_week] = {}
                weekly_variants_by_region[data_week] = {}
            if region not in weekly_cases_by_region[data_week]:
                weekly_cases_by_region[data_week][region] = int(float(fields[cases_index]))
                total_cases += int(float(fields[cases_index]))
                weekly_variants_by_region[data_week][region] = int(float(fields[variants_index]))
                total_variants += int(float(fields[variants_index]))

with open('uk-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for region in regional_abbreviations:
        abbrev = regional_abbreviations[region]
        for dat in ['pt','qt']:
            hbuff.append(abbrev + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)

    # no data until Sept 7
    while the_date < date(2020,9,7):
        date_str = the_date.isoformat()
        buff = [date_str]
        for region in regional_abbreviations:
            buff.append('')
            buff.append('')
        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)

    cumulative_cases={}
    cumulative_variants={}
    for region in regional_abbreviations:
        cumulative_cases[region] = 0
        cumulative_variants[region] = 0

    for data_week in weekly_cases_by_region:
        # use equal numbers per day, with additional on first days of week
        daily_cases = {}
        daily_cases_xtra = {}
        daily_variants = {}
        daily_variants_xtra = {}
        for region in regional_abbreviations:
            if region != 'England':
                daily_cases_xtra[region] = weekly_cases_by_region[data_week][region] % 7
                daily_cases[region] = (weekly_cases_by_region[data_week][region]-daily_cases_xtra[region]) / 7
                daily_variants_xtra[region] = weekly_variants_by_region[data_week][region] % 7
                daily_variants[region] = (weekly_variants_by_region[data_week][region] - daily_variants_xtra[region]) / 7
        for i in range(7):
            date_str = the_date.isoformat()
            buff = [date_str]
            cases_sum = 0
            variants_sum = 0
            for region in regional_abbreviations:
                if region != 'England':
                    cumulative_cases[region] += daily_cases[region]
                    cumulative_variants[region] += daily_variants[region]
                    cases_sum += daily_cases[region]
                    variants_sum += daily_variants[region]
                    if i < daily_cases_xtra[region]:
                        cumulative_cases[region] += 1
                        cases_sum += 1
                    if i < daily_variants_xtra[region]:
                        cumulative_variants[region] += 1
                        variants_sum += 1
                else:
                    cumulative_cases[region] += cases_sum
                    cumulative_variants[region] += variants_sum

                buff.append(str(cumulative_cases[region]))
                buff.append(str(cumulative_variants[region]))

            the_file.write(','.join(buff) + '\n')
            the_date += timedelta(days=1)

print('Total cases =',total_cases,' total variants=',total_variants)