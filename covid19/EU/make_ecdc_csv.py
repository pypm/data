# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import timedelta

t0 = datetime.date(2020,3,1)

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

# Starting Nov 8 2021, multiple sources: daily scraped.csv, daily non-eu, weekly for remaining
data_by_state = {}
last_date_by_state = {}

# Starting Oct 9 2022, ECDC data stale, use OWID repo and UK data to continue updating data
owid_start_date = datetime.date(2022, 9, 4)
owid_states = ['BE', 'FR', 'IE', 'NO', 'CH']
uk_start_date = datetime.date(2022, 9, 4)

raw_files = ['scraped.csv','non-eu.csv']
date_fields = [3,2]
value_fields = [4,3]

record_date = None
for j,raw_file in enumerate(raw_files):
    with open(raw_file) as f:
        for i,line in enumerate(f):
            if i > 0:
                fields = line.split(',')
                if j>0 or fields[2] == 'New_Hospitalised':
                    df = fields[date_fields[j]].split('-')
                    record_date = datetime.date(int(df[0]),int(df[1]),int(df[2]))
                    state = fields[1]
                    value = int(fields[value_fields[j]])

                    if state not in data_by_state:
                        data_by_state[state] = {}
                        data_by_state[state][t0] = 0
                        last_date_by_state[state] = t0
                    if record_date <= t0:
                        data_by_state[state][t0] += value
                    else:
                        data_by_state[state][record_date] = value
                    if record_date > last_date_by_state[state]:
                        last_date_by_state[state] = record_date

print('Daily hospitalization data taken in scraped.csv and non-eu.csv up to (last date):')
raw_states = []
bad_states = []
for state in data_by_state:
    print(state, last_date_by_state[state])
    #if raw data is out of date, do not use it
    if (datetime.date.today()-last_date_by_state[state]).days > 120:
        print(state,' ** raw data not used ** too old')
        bad_states.append(state)
    else:
        raw_states.append(state)

for state in bad_states:
    del data_by_state[state]
    del last_date_by_state[state]

# use OWID data to fill in values, starting from owid_start_date
# OWID is 7 day sum (typically updated daily) so that daily admissions can be extracted
# Otherwise use weekly values to update

owid_file = 'covid-hospitalizations.csv'

last_state = ''
last_date = ''
seven_day_buffer = []
with open(owid_file) as f:
    for i, line in enumerate(f):
        if i > 0:
            fields = line.strip().split(',')
            if fields[3] == 'Weekly new hospital admissions':
                country = fields[0]
                if country in regional_abbreviations:
                    state = regional_abbreviations[country]
                    if state != last_state:
                        seven_day_buffer = []
                    last_state = state
                    if state in owid_states:
                        df = fields[2].split('-')
                        record_date = datetime.date(int(df[0]), int(df[1]), int(df[2]))
                        if record_date == owid_start_date:
                            last_date = record_date
                            seven_day_buffer = []
                            for day_offset in range(-6,1,1):
                                date = record_date + timedelta(days=day_offset)
                                value = data_by_state[state][date]
                                seven_day_buffer.append(value)
                        elif record_date > owid_start_date:
                            value = int(float(fields[4]))
                            if (record_date-last_date).days == 1:
                                new_admin = value - int(np.sum(seven_day_buffer[1:]))
                                data_by_state[state][record_date] = new_admin
                                seven_day_buffer = seven_day_buffer[1:] + [new_admin]
                                last_date = record_date
                            else:
                                if len(seven_day_buffer) == 0:
                                    seven_day_buffer = []
                                    for day_offset in range(-6, 1, 1):
                                        date = record_date + timedelta(days=day_offset)
                                        value = data_by_state[state][date]
                                        seven_day_buffer.append(value)
                                days = (record_date-last_date).days
                                new_admin = value - np.sum(seven_day_buffer[days:])
                                daily = int(new_admin / days)
                                extra = new_admin % days
                                for iday in range(days):
                                    date = record_date - timedelta(days=iday)
                                    data_by_state[state][date] = daily
                                    if iday < extra:
                                        data_by_state[state][date] += 1
                                last_date = record_date

                        if record_date > last_date_by_state[state]:
                            last_date_by_state[state] = record_date

# use weekly data for the rest: split across days of week
ecdc_file = 'truth_ECDC-Incident Hospitalizations.csv'

date_error = None
record_date = None
with open(ecdc_file) as f:
    for i,line in enumerate(f):
        if i > 0:
            fields = line.split(',')
            df = fields[2].split('-')
            record_date = datetime.date(int(df[0]),int(df[1]),int(df[2]))
            state = fields[1]
            value = int(fields[3])

            if record_date.weekday() != 5:
                if date_error is not None:
                    date_error = state + ' : ' + record_date.isoformat()

            if state not in raw_states:

                if state not in data_by_state:
                    data_by_state[state] = {}
                    data_by_state[state][t0] = 0
                    last_date_by_state[state] = t0
                if record_date <= t0:
                    data_by_state[state][t0] += value
                else:
                    daily = int(value/7)
                    extra = value%7
                    for iday in range(7):
                        date = record_date - timedelta(days=iday)
                        data_by_state[state][date] = daily
                        if iday < extra:
                            data_by_state[state][date] += 1
                if record_date > last_date_by_state[state]:
                    last_date_by_state[state] = record_date

if date_error is not None:
    print(' *** Error in weekly data:',date_error)

print('Weekly Hospitalization data provided up to (last date):')
last_date = t0
for state in data_by_state:
    if last_date_by_state[state]>last_date:
        last_date = last_date_by_state[state]
    if state not in raw_states:
        print(state, last_date_by_state[state])

with open('eu-ecdc-pypm.csv', 'w') as the_file:

    data_started = {}
    previous_value = {}
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
            if state in data_by_state:
                if the_date in data_by_state[state]:
                    if state not in data_started:
                        data_started[state] = True
                    value = str(data_by_state[state][the_date])
                    previous_value[state] = value
                elif data_started[state]:
                    value = previous_value[state]
            buff.append(value)

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
