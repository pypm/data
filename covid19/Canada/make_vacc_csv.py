# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
        'BC': 'BC',
        'Alberta': 'AB',
        'Saskatchewan': 'SK',
        'Manitoba': 'MB',
        'Ontario': 'ON',
        'Quebec': 'QC',
        'New Brunswick': 'NB',
        'Newfoundland': 'NL',
        'Nova Scotia': 'NS',
        'PEI': 'PE',
        'Yukon': 'YT',
        'NWT': 'NT',
        'Nunavut': 'NU'
    }

states = ['BC','AB','SK','MB','ON','QC','NB','NL','NS','PE','YT','NT','NU']

n_days = 0
vacc_by_state = {}
t0 = date(2020,3,1)
last_date = '2020-03-01'

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
                    vacc_by_state[state][data_date] = fields[dose1_index]

with open('ca-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in ['xt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)
    done = False
    while not done:
        date_str = the_date.isoformat()
        buff = [date_str]
        for state in states:
            if date_str in vacc_by_state[state]:
                val = vacc_by_state[state][date_str]
                if val != '' and int(val) > 0:
                    buff.append(vacc_by_state[state][date_str])
                else:
                    buff.append('')
            else:
                buff.append('')

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
        done = date_str == last_date
