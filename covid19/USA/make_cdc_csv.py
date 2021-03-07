# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

def get_infected(state,day):
    infected = 0
    if day >= range_by_state[state][0] and day <= range_by_state[state][1]:
        data = nt_by_state[state]
        period_before = None
        period_after = None
        for period in data:
            if day > period['end']:
                period_before = period
            if period_after is None and day < period['start']:
                period_after = period
            if day >= period['start'] and day <= period['end']:
                infected = period['infected']
                break
        # do linear interpolation for missing parts
        if infected == 0:
            inf_b = period_before['infected']
            inf_a = period_after['infected']
            d_b = period_before['end']
            d_a = period_after['start']
            r_inf = inf_b + 1.*(day - d_b)/(d_a - d_b)*(inf_a - inf_b)
            infected = int(r_inf)

    str_inf = ''
    if infected !=0:
        str_inf = str(infected)
    return str_inf

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

nt_by_state = {}
t0 = date(2020,3,1)

with open('Nationwide_Commercial_Laboratory_Seroprevalence_Survey.csv') as f:

    for i,line in enumerate(f):
        if i > 0:
            fix_line = ' '.join(line.split())
            groups = fix_line.split('"')
            cols_0 = groups[0].split(',')
            state = cols_0[0]

            cols_1 = groups[1].split(',')
            if len(cols_1) == 2: # dates within one year
                date_range = cols_1[0]
                day_range = date_range.split(',')[0]
                year_start = cols_1[1].split(' ')[1]
                year_end = year_start
                day_cols = day_range.split(' ')
                month_start = day_cols[0]
                day_start = day_cols[1]
                month_end = day_cols[3]
                day_end = day_cols[4]
            else:
                month_start = cols_1[0].split(' ')[0]
                day_start = cols_1[0].split(' ')[1]
                year_start = cols_1[1].strip().split(' ')[0]
                month_end = cols_1[1].strip().split(' ')[2]
                day_end = cols_1[1].strip().split(' ')[3]
                year_end = cols_1[2].strip()

            start = datetime.strptime(' '.join([month_start,day_start,year_start]), '%b %d %Y').date()
            end = datetime.strptime(' '.join([month_end,day_end,year_end]), '%b %d %Y').date()

            start_day = (start-t0).days
            end_day = (end-t0).days

            infected = groups[2].split(',')[40]
            if infected != '' and int(infected) != 0:
                nt_data = {'start':start_day, 'end':end_day, 'infected':int(infected)}

                if state not in nt_by_state:
                    nt_by_state[state] = [nt_data]
                else:
                    nt_by_state[state].append(nt_data)

range_by_state = {}
last_day = 0
for state in nt_by_state:
    data = nt_by_state[state]
    first = 500
    last = 0
    for period in data:
        first = min(first,period['start'])
        last = max(last,period['end'])
        last_day = max(last_day,period['end'])
    range_by_state[state] = [first,last]

with open('usa-cdc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in nt_by_state:
        for dat in ['nt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)
    n_days = last_day
    for i in range(n_days):
        buff = [the_date.isoformat()]
        for state in nt_by_state:
            buff.append(get_infected(state,i))

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
