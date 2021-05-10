# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import datetime, date, timedelta

regional_abbreviations = {
        'Baden-Wurttemberg':'bw',
        'Bavaria':'by',
        'Berlin':'be',
        'Brandenburg':'bb',
        'Bremen':'hb',
        'Hamburg':'hh',
        'Hesse':'he',
        'Lower Saxony':'ni',
        'Mecklenburg-Vorpommern':'mv',
        'North Rhine-Westphalia':'nw',
        'Rhineland-Palatinate':'rp',
        'Saarland':'sl',
        'Saxony':'sn',
        'Saxony-Anhalt':'st',
        'Schleswig-Holstein':'sh',
        'Thuringia':'th'
    }

states = ['bw','by','be','bb','hb','hh','he','ni','mv','nw','rp','sl','sn','st','sh','th']

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
            if key[0:3] == 'DE_':
                state = key[3:5].lower()
                if state in states:
                    data_date = fields[0]
                    if data_date > last_date:
                        last_date = data_date
                    if state not in vacc_by_state:
                        vacc_by_state[state] = {}
                    vacc_by_state[state][data_date] = fields[dose1_index]

# Add weekly data from https://impfdashboard.de/daten
# *** note: need to switch order of mv and ni in data ***

data_dates = []
datas = []

data_dates.append('2021-05-02')
datas.append([3084030,3786154, 952267,644240,200593,527133,1704620,2282000,485297,5313732,1134694,309836,1047705,622836,777485,561630])

data_dates.append('2021-05-09')
datas.append([3567730,4381270,1090630,725504,232341,605130,2048352,2710302,562619,6210075,1286872,363731,1174652,708859,889448,638408,])

for i,data_date in enumerate(data_dates):
    last_date = data_date
    for istate, state in enumerate(states):
        vacc_by_state[state][data_date] = str(datas[i][istate])

with open('germany-vacc-pypm.csv', 'w') as the_file:

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
