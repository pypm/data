# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
    'Austria': 'AT',
    'Belgium': 'BE',
    'Bulgaria': 'BG',
    'Croatia': 'HR',
    'Cyprus': 'CY',
    'Czechia': 'CZ',
    'Denmark': 'DK',
    'Estonia': 'EE',
    'Finland': 'FI',
    'France': 'FR',
    'Germany': 'DE',
    'Greece': 'GR',
    'Hungary': 'HU',
    'Iceland': 'IS',
    'Ireland': 'IE',
    'Italy': 'IT',
    'Latvia': 'LV',
    'Liechtenstein': 'LI',
    'Lithuania': 'LT',
    'Luxembourg': 'LU',
    'Malta': 'MT',
    'Netherlands': 'NL',
    'Norway': 'NO',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Romania': 'RO',
    'Slovakia': 'SK',
    'Slovenia': 'SI',
    'Spain': 'ES',
    'Sweden': 'SE',
    'Switzerland': 'CH',
    'United Kingdom': 'GB'
}

states = ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LI','LT','LU','MT',
          'NL','NO','PL','PT','RO','SK','SI','ES','SE','CH','GB']

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
            state = fields[1]
            if state in states:
                data_date = fields[0]
                if data_date > last_date:
                    last_date = data_date
                if state not in vacc_by_state:
                    vacc_by_state[state] = {}
                vacc_by_state[state][data_date] = fields[dose1_index]

with open('eu-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in ['xt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)
    last_val = {}
    done = False
    while not done:
        date_str = the_date.isoformat()
        buff = [date_str]
        for state in states:
            if date_str in vacc_by_state[state]:
                val = vacc_by_state[state][date_str]
                if val != '' and int(val) > 0:
                    buff.append(val)
                    last_val[state] = val
                elif state in last_val:
                    buff.append(last_val[state])
                else:
                    buff.append('')
            elif state in last_val:
                buff.append(last_val[state])
            else:
                buff.append('')

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
        done = date_str == last_date
