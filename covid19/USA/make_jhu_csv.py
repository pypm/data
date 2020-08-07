# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import timedelta

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

pt_by_state = {}
with open('time_series_covid19_confirmed_US.csv') as f:

    for line in f:
        groups = line.split('"')
        if len(groups) == 3:
            cols = groups[0].split(',')
            state_name = cols[6]
            if state_name in regional_abbreviations:
                state = regional_abbreviations[state_name]
                sdata = groups[2].split(',')[40:]
                data = [int(s) for s in sdata]
                if state not in pt_by_state:
                    pt_by_state[state] = np.array(data)
                else:
                    pt_by_state[state] += np.array(data)

dt_by_state = {}
with open('time_series_covid19_deaths_US.csv') as f:

    for line in f:
        groups = line.split('"')
        if len(groups) == 3:
            cols = groups[0].split(',')
            state_name = cols[6]
            if state_name in regional_abbreviations:
                state = regional_abbreviations[state_name]
                sdata = groups[2].split(',')[40:]
                data = [int(s) for s in sdata]
                if state not in dt_by_state:
                    dt_by_state[state] = np.array(data)
                else:
                    dt_by_state[state] += np.array(data)


with open('usa-jhu-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in ['pt','dt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = datetime.date(2020,3,1)
    n_days = len(pt_by_state['AL'])
    for i in range(n_days):
        buff = [the_date.isoformat()]
        for state in states:
            buff.append(str(pt_by_state[state][i]))
            buff.append(str(dt_by_state[state][i]))

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)

