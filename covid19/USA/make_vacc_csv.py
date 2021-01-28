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

with open('vacc_num.csv') as f:

    for i,line in enumerate(f):
        if i == 0:
            header = line.split(',')
            n_days = len(header)-3
        else:
            fields = line.split(',')
            location = fields[1].split('|')
            if len(location) > 1:
                state = location[1].strip()
                abbrev = regional_abbreviations[state]
                vacc_by_state[abbrev] = fields[2:-1]

with open('usa-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in ['xt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)
    first = 365 - 28 - 31
    for i in range(first+n_days):
        buff = [the_date.isoformat()]
        for state in states:
            if i<first:
                buff.append('')
            else:
                val = vacc_by_state[state][i-first]
                if val == '0':
                    buff.append('')
                else:
                    buff.append(val)

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
