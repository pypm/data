# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import timedelta

t0 = datetime.date(2020,3,1)
last_date = datetime.date(2020,3,1)

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

hd_by_state = {}

ecdc_file = 'truth_ECDC-Incident Hospitalizations.csv'
data_by_state = {}

record_date = None
with open(ecdc_file) as f:
    for i,line in enumerate(f):
        if i > 0:
            fields = line.split(',')
            df = fields[0].split('-')
            record_date = datetime.date(int(df[0]),int(df[1]),int(df[2]))
            state = fields[1]
            value = int(fields[3])

            if state not in data_by_state:
                data_by_state[state] = {}
                data_by_state[state][t0] = 0
            if record_date <= t0:
                data_by_state[state][t0] += value
            else:
                data_by_state[state][record_date] = value
            if record_date > last_date:
                last_date = record_date

print('Hospitalization data provided for:')
print(','.join(list(data_by_state.keys())))

with open('eu-ecdc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for country in regional_abbreviations:
        state = regional_abbreviations[country]
        hbuff.append(state + '-hd')
    the_file.write(','.join(hbuff) + '\n')

    the_date = datetime.date(2020,3,1)
    while the_date <= last_date:
        buff = [the_date.isoformat()]
        for country in regional_abbreviations:
            state = regional_abbreviations[country]
            value = ''
            if state in data_by_state and the_date in data_by_state[state]:
                value = str(data_by_state[state][the_date])
            buff.append(value)

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
