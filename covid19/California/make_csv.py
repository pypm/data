# -*- coding: utf-8 -*-
"""
Convert California case/death by age data

Note: after running this, must fix the .pypm file: remove duplicate entry for May 17:
and add missing fields for that date:
3330 0 40500 188

Also get hospitalization data by age group

@author: karlen
"""
import datetime

d_d = {'totalpositive': ['pt', 'Total cases'],
       'deaths': ['dt', 'Total deaths']}
col_d = {}

states = ['0-17','18-49','50-64','65+']

i = 0

last_date = 0
col_d = {}
dict_by_date = {}
dict_by_state = {}
date_list = []
with open('case_demographics_age.csv') as f:
    for line in f:
        cols = line.split(',')
        if i == 0:
            j = 0
            for col in cols:
                if col in d_d:
                    col_d[j] = d_d[col][0]
                j += 1
        else:
            date = cols[2]
            state = cols[0]
            if state == '65 and Older':
                state = '65+'
            if date != last_date and last_date != 0:
                dict_by_date[last_date] = dict_by_state
                date_list.append(last_date)
                dict_by_state = {}

            dict_by_datum = {}
            for i_col in col_d:
                dict_by_datum[col_d[i_col]] = str(cols[i_col])
            dict_by_state[state] = dict_by_datum
            last_date = date
        i += 1

if len(dict_by_state) > 0:
    dict_by_date[last_date] = dict_by_state
    date_list.append(last_date)

datums = []
for key in col_d:
    datums.append(col_d[key])

group_pop = {'0-17': 8.8875, '18-49': 17.222, '50-64': 7.268, '65+':6.2015}
cdc_name = {'< 18':'0-17', '18-49 yr':'18-49', '50-64 yr':'50-64', '65+ yr':'65+'}
hosp_by_week = {'0-17':{}, '18-49':{}, '50-64':{}, '65+':{}}

with open('COVID-19Surveillance_All_Data.csv') as f:
    for line in f:
        cols = line.rstrip().split(',')
        if len(cols) > 9:
            if cols[0] == 'California':
                if cols[5] in cdc_name:
                    if cols[6]=='Overall' and cols[7]=='Overall':
                        week = int(cols[4])
                        if cols[8] != 'null':
                            hosp_count = float(cols[8])*10.*group_pop[cdc_name[cols[5]]]
                            hosp_by_week[cdc_name[cols[5]]][week] = '{0:.1f}'.format(hosp_count)

with open('california-pypm.csv', 'w') as the_file:
    hbuff = ['date']
    for state in states:
        for dat in datums:
            hbuff.append(state + '-' + dat)
        hbuff.append(state + '-ht')
    the_file.write(','.join(hbuff) + '\n')

    date_list.sort()
    for day in range(1,32,1):
        the_file.write('2020-03-'+str(day).zfill(2) + '\n')
    the_file.write('2020-04-01' + '\n')

    for date in date_list:
        if date > '2020-02-29':
            parts = date.split('-')
            week = datetime.date(int(parts[0]), int(parts[1]), int(parts[2])).isocalendar()[1]
            dict_by_state = dict_by_date[date]
            buff = [date]
            for state in states:
                dict_by_datum = None
                if state in dict_by_state:
                    dict_by_datum = dict_by_state[state]
                for dat in datums:
                    val = ''
                    if dict_by_datum is not None:
                        val = dict_by_datum[dat]
                    buff.append(val)
                if week in hosp_by_week[state]:
                    buff.append(hosp_by_week[state][week])
                else:
                    buff.append('')
            the_file.write(','.join(buff) + '\n')
