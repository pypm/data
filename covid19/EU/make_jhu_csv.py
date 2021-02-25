# -*- coding: utf-8 -*-
"""

@author: karlen
"""
import numpy as np
import datetime
from datetime import timedelta

t0 = datetime.date(2020,3,1)

pd_by_state = {}

jhu_files = {'pt':'truth_JHU-Incident Cases.csv','dt':'truth_JHU-Incident Deaths.csv'}
inc_data = {}

record_date = None
for data_id in jhu_files:
    with open(jhu_files[data_id]) as f:
        data_by_state = {}
        for i,line in enumerate(f):
            if i > 0:
                fields = line.split(',')
                df = fields[2].split('-')
                record_date = datetime.date(int(df[0]),int(df[1]),int(df[2]))
                state = fields[0]
                value = int(fields[3])

                if state not in data_by_state:
                    data_by_state[state] = {}
                    data_by_state[state][t0] = 0
                if record_date <= t0:
                    data_by_state[state][t0] += value
                else:
                    data_by_state[state][record_date] = value
        inc_data[data_id] = data_by_state


with open('eu-jhu-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    cumul = {}
    for state in inc_data['pt']:
        cumul[state] = {}
        for data_id in jhu_files:
            cumul[state][data_id] = 0
            hbuff.append(state + '-' + data_id)
    the_file.write(','.join(hbuff) + '\n')

    the_date = datetime.date(2020,3,1)
    while the_date <= record_date:
        buff = [the_date.isoformat()]
        for state in inc_data['pt']:
            for data_id in jhu_files:
                value = inc_data[data_id][state][the_date]
                cumul[state][data_id] += value
                buff.append(str(cumul[state][data_id]))

        the_file.write(','.join(buff) + '\n')
        the_date += timedelta(days=1)
