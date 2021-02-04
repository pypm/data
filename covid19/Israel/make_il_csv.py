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
    'Unknown': 'xx',
    'All':'il'
}

age_group_dict = {
    '0-19':'19',
    '20-24':'20',
    '25-29':'20',
    '30-34':'30',
    '35-39':'30',
    '40-44':'40',
    '45-49':'40',
    '50-54':'50',
    '55-59':'50',
    '60-64':'60',
    '65-69':'60',
    '70-74':'70',
    '75-79':'70',
    '80+':'80',
    'NULL':'xx'
}

total_cases = 0
total_deaths = 0
weekly_case_by_age = {}
weekly_death_by_age = {}
t0 = date(2020,3,1)
last_week = '2020-03-01'

input_files = ['age-and-sex-march-september.csv','corona_age_and_gender.csv']

for i, input_file in enumerate(input_files):
    with open(input_file, errors="ignore") as f:

        for j,line in enumerate(f):
            if j == 0:
                header = line.strip().split(',')
                age_index = header.index('age_group')
                cases_index = header.index('weekly_cases')
                deaths_index = header.index('weekly_deceased')
            else:
                fields = line.strip().split(',')
                data_week = None
                if i == 0:
                    data_week_text = fields[0].split('/')
                    data_week = '-'.join(list(reversed(data_week_text)))
                else:
                    data_week = fields[0]

                age_text = fields[2]
                age_group = age_group_dict[age_text]
                if data_week not in weekly_case_by_age:
                    weekly_case_by_age[data_week] = {}
                    weekly_death_by_age[data_week] = {}
                if age_group not in weekly_case_by_age[data_week]:
                    weekly_case_by_age[data_week][age_group] = 0
                    weekly_death_by_age[data_week][age_group] = 0
                if fields[cases_index] != '<15':
                    weekly_case_by_age[data_week][age_group] += int(float(fields[cases_index]))
                    total_cases += int(float(fields[cases_index]))
                if fields[deaths_index] != '<15':
                    weekly_death_by_age[data_week][age_group] += int(float(fields[deaths_index]))
                    total_deaths += int(float(fields[deaths_index]))

with open('il-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for group in regional_abbreviations:
        abbrev = regional_abbreviations[group]
        for dat in ['pt','dt']:
            hbuff.append(abbrev + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)

    # no data for the first 14 days of March
    for i in range(14):
        date_str = the_date.isoformat()
        buff = [date_str]
        for group in regional_abbreviations:
            buff.append('')
            buff.append('')
        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)

    cumulative_case={}
    cumulative_death={}
    for group in regional_abbreviations:
        age_group = regional_abbreviations[group]
        cumulative_case[age_group] = 0
        cumulative_death[age_group] = 0

    for data_week in weekly_case_by_age:
        # use equal numbers per day, with additional on first days of week
        daily_case = {}
        daily_case_xtra = {}
        daily_death = {}
        daily_death_xtra = {}
        for group in regional_abbreviations:
            if group != 'All':
                age_group = regional_abbreviations[group]
                daily_case_xtra[age_group] = weekly_case_by_age[data_week][age_group] % 7
                daily_case[age_group] = (weekly_case_by_age[data_week][age_group]-daily_case_xtra[age_group]) / 7
                daily_death_xtra[age_group] = weekly_death_by_age[data_week][age_group] % 7
                daily_death[age_group] = (weekly_death_by_age[data_week][age_group] - daily_death_xtra[age_group]) / 7
        for i in range(7):
            date_str = the_date.isoformat()
            buff = [date_str]
            case_sum = 0
            death_sum = 0
            for group in regional_abbreviations:
                age_group = regional_abbreviations[group]
                if group != 'All':
                    cumulative_case[age_group] += daily_case[age_group]
                    cumulative_death[age_group] += daily_death[age_group]
                    case_sum += daily_case[age_group]
                    death_sum += daily_death[age_group]
                    if i < daily_case_xtra[age_group]:
                        cumulative_case[age_group] += 1
                        case_sum += 1
                    if i < daily_death_xtra[age_group]:
                        cumulative_death[age_group] += 1
                        death_sum += 1
                else:
                    cumulative_case[age_group] += case_sum
                    cumulative_death[age_group] += death_sum

                buff.append(str(cumulative_case[age_group]))
                buff.append(str(cumulative_death[age_group]))

            the_file.write(','.join(buff) + '\n')
            the_date += timedelta(days=1)

print('Total cases =',total_cases,' total deaths=',total_deaths)