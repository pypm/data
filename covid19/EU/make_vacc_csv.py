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
vacc_by_state_week = {}
t0 = date(2020,3,1)
last_date = '2020-03-01'

vacc_data = 'ecdc'

if vacc_data == 'google':

    with open('../vaccinations.csv') as f:

        for i, line in enumerate(f):
            if i == 0:
                header = line.split(',')
                dose1_index = header.index('cumulative_persons_vaccinated')
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

elif vacc_data == 'ecdc':
    with open('ecdc-vaccinations.csv') as f:
        dose_indices = []
        for i, line in enumerate(f):
            if i == 0:
                header = line.split(',')
                yearweek_index = header.index('YearWeekISO')
                country_index = header.index('ReportingCountry')
                region_index = header.index('Region')
                group_index = header.index('TargetGroup')
                for text in ['FirstDose','SecondDose','DoseAdditional1','DoseAdditional2',
                             'DoseAdditional3','UnknownDose']:
                    dose_indices.append(header.index(text))
            else:
                fields = line.split(',')
                year = int(fields[yearweek_index].split('-')[0])
                if year >= 2022:
                    yearweek = fields[yearweek_index]
                    state = fields[country_index]
                    region = fields[region_index]
                    group = fields[group_index]
                    if state in states and region == state and group == 'ALL':
                        if state not in vacc_by_state_week:
                            vacc_by_state_week[state] = {}
                        if yearweek not in vacc_by_state_week[state]:
                            vacc_by_state_week[state][yearweek] = 0
                        for dose_index in dose_indices:
                            doses = int(fields[dose_index])
                            vacc_by_state_week[state][yearweek] += doses

    epiweek1 = {'2022':date(2022,1,2),'2023':date(2023,1,1)}
    for state in vacc_by_state_week:
        vacc_by_state[state] = {}
        cumul_vacc = 0
        yearweeks = list(vacc_by_state_week[state].keys())
        yearweeks.sort()
        for yearweek in yearweeks:
            year = yearweek.split('-')[0]
            week = int(yearweek.split('W')[1])
            start_day = epiweek1[year] + timedelta(days=7*(week-1))
            daily = int(vacc_by_state_week[state][yearweek]/7)
            for day in range(7):
                date_str = (start_day+timedelta(days=day)).isoformat()
                cumul_vacc += daily
                vacc_by_state[state][date_str] = str(cumul_vacc)
                if date_str > last_date:
                    last_date = date_str

with open('eu-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in vacc_by_state:
        for dat in ['xt']:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    the_date = date(2020,3,1)
    last_val = {}
    done = False
    while not done:
        date_str = the_date.isoformat()
        buff = [date_str]
        for state in vacc_by_state:
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
