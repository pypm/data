# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
        'Alaska':'AK',
        'Alabama':'AL',
        'Arkansas':'AR',
        'American Samoa':'AS',
        'Arizona':'AZ',
        'California':'CA',
        'Colorado':'CO',
        'Connecticut':'CT',
        'District of Columbia':'DC',
        'Delaware':'DE',
        'Florida':'FL',
        'Georgia':'GA',
        'Guam':'GU',
        'Hawaii':'HI',
        'Iowa':'IA',
        'Idaho':'ID',
        'Illinois':'IL',
        'Indiana':'IN',
        'Kansas':'KS',
        'Kentucky':'KY',
        'Louisiana':'LA',
        'Massachusetts':'MA',
        'Maryland':'MD',
        'Maine':'ME',
        'Michigan':'MI',
        'Minnesota':'MN',
        'Missouri':'MO',
        'Northern Mariana Islands':'MP',
        'Mississippi':'MS',
        'Montana':'MT',
        'North Carolina':'NC',
        'North Dakota':'ND',
        'Nebraska':'NE',
        'New Hampshire':'NH',
        'New Jersey':'NJ',
        'New Mexico':'NM',
        'Nevada':'NV',
        'New York':'NY',
        'Ohio':'OH',
        'Oklahoma':'OK',
        'Oregon':'OR',
        'Pennsylvania':'PA',
        'Puerto Rico':'PR',
        'Rhode Island':'RI',
        'South Carolina':'SC',
        'South Dakota':'SD',
        'Tennessee':'TN',
        'Texas':'TX',
        'Utah':'UT',
        'Virginia':'VA',
        'Virgin Islands':'VI',
        'Vermont':'VT',
        'Washington':'WA',
        'Wisconsin':'WI',
        'West Virginia':'WV',
        'Wyoming':'WY'
        }

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS',
          'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY',
          'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']

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
            if key[0:3] == 'US_' and len(key)==5:
                state = key[3:5]
                if state in states:
                    data_date = fields[0]
                    if data_date > last_date:
                        last_date = data_date
                    if state not in vacc_by_state:
                        vacc_by_state[state] = {}
                    vacc_by_state[state][data_date] = fields[dose1_index]

with open('usa-vacc-pypm.csv', 'w') as the_file:

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
