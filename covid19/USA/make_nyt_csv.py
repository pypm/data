# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import timedelta

regional_abbreviations = {
    'Alaska': 'AK',
    'Alabama': 'AL',
    'Arkansas': 'AR',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'District of Columbia': 'DC',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Iowa': 'IA',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Massachusetts': 'MA',
    'Maryland': 'MD',
    'Maine': 'ME',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Missouri': 'MO',
    'Northern Mariana Islands': 'MP',
    'Mississippi': 'MS',
    'Montana': 'MT',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Nebraska': 'NE',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'Nevada': 'NV',
    'New York': 'NY',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Virginia': 'VA',
    'Virgin Islands': 'VI',
    'Vermont': 'VT',
    'Washington': 'WA',
    'Wisconsin': 'WI',
    'West Virginia': 'WV',
    'Wyoming': 'WY'
}

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN',
          'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI',
          'WV', 'WY']

pt_by_state = {}
dt_by_state = {}
last_date = ''
with open('us-states.csv') as f:
    for i, line in enumerate(f):
        cols = line.strip().split(',')
        state_name = cols[1]
        if state_name in regional_abbreviations:
            state = regional_abbreviations[state_name]
            if state not in pt_by_state:
                pt_by_state[state] = {}
                dt_by_state[state] = {}
            date = cols[0]
            if date in pt_by_state[state]:
                print('Duplicate entry for', state_name, date)
            else:
                pt_by_state[state][date] = cols[3]
                dt_by_state[state][date] = cols[4]
            last_date = date

with open('usa-nyt-pypm.csv', 'w') as the_file:
    hbuff = ['date']
    for state in states:
        for dat in ['pt', 'dt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = datetime.date(2020, 3, 1)
    while the_date.isoformat() <= last_date:
        date = the_date.isoformat()
        buff = [date]
        for state in states:
            if date not in pt_by_state[state]:
                buff.append('0')
                buff.append('0')
            else:
                buff.append(str(pt_by_state[state][date]))
                buff.append(str(dt_by_state[state][date]))

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
