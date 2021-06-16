# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
        'British Columbia': 'BC',
        'Alberta': 'AB',
        'Saskatchewan': 'SK',
        'Manitoba': 'MB',
        'Ontario': 'ON',
        'Quebec': 'QC',
        'New Brunswick': 'NB',
        'Newfoundland and Labrador': 'NL',
        'Nova Scotia': 'NS',
        'Prince Edward Island': 'PE',
        'Yukon': 'YT',
        'Northwest Territories': 'NT',
        'Nunavut': 'NU'
    }

states = ['BC','AB','SK','MB','ON','QC','NB','NL','NS','PE','YT','NT','NU']

n_days = 0
vacc_by_state = {}
t0 = date(2020,3,1)
last_date = '2020-03-01'

source = 'infobase'
# https://health-infobase.canada.ca/src/data/covidLive/vaccination-coverage-byAgeAndSex.csv

if source == 'infobase':
    with open('vaccination-coverage-byAgeAndSex.csv') as f:
        for i, line in enumerate(f):
            if i == 0:
                header = line.split(',')
                state_index = header.index('prename')
                date_index = header.index('week_end')
                dose1_index = header.index('numtotal_atleast1dose')
                age_index = header.index('age')
            else:
                fields = line.split(',')
                if fields[state_index] in regional_abbreviations:
                    state = regional_abbreviations[fields[state_index]]
                    if fields[age_index] == 'All ages':
                        if fields[dose1_index] != 'na':
                            data_date = fields[date_index]
                            if data_date > last_date:
                                last_date = data_date
                            if state not in vacc_by_state:
                                vacc_by_state[state] = {}
                            if data_date not in vacc_by_state[state]:
                                vacc_by_state[state][data_date] = 0
                            vacc_by_state[state][data_date] += int(fields[dose1_index])

elif source == 'google':
    with open('../vaccinations.csv') as f:

        for i, line in enumerate(f):
            if i == 0:
                header = line.split(',')
                dose1_index = header.index('total_persons_vaccinated')
            else:
                fields = line.split(',')
                key = fields[1]
                if key[0:3] == 'CA_':
                    state = key[3:5]
                    if state in states:
                        data_date = fields[0]
                        if data_date > last_date:
                            last_date = data_date
                        if state not in vacc_by_state:
                            vacc_by_state[state] = {}
                        vacc_by_state[state][data_date] = int(fields[dose1_index])

with open('ca-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in ['xt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)
    done = False
    started = {}
    previous_buff = None
    while not done:
        date_str = the_date.isoformat()
        buff = [date_str]
        for state in states:
            if date_str in vacc_by_state[state]:
                val = str(vacc_by_state[state][date_str])
            else:
                val = ''

            if val != '' and int(val) > 0:
                started[state] = True
                buff.append(str(vacc_by_state[state][date_str]))
            elif state in started:
                # repeat value from previous line in current column
                buff.append(previous_buff[len(buff)])
            else:
                buff.append('')


        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
        previous_buff = buff
        done = date_str == last_date
