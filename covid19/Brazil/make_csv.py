# -*- coding: utf-8 -*-
"""
Convert Brazil data

@author: karlen
"""

d_d={'totalCases':['pt','Total cases'],
'deaths':['dt','Total deaths']}
col_d ={}

states = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI',
          'RJ','RN','RS','RO','RR','SC','SP','SE','TO']

i=0

last_date = 0
col_d = {}
dict_by_date = {}
dict_by_state = {}
date_list = []
with open('cases-brazil-states.csv') as f:
    for line in f:
        cols = line.split(',')
        if i == 0:
            j=0
            for col in cols:
                if col in d_d:
                    col_d[j]=d_d[col][0]
                j+=1
        else:
            date = cols[0]
            state = cols[2]
            if date != last_date and last_date !=0:
                dict_by_date[last_date] = dict_by_state
                date_list.append(last_date)
                dict_by_state = {}

            dict_by_datum = {}
            for i_col in col_d:
                dict_by_datum[col_d[i_col]] = str(cols[i_col])
            dict_by_state[state] = dict_by_datum
            last_date = date
        i+=1

if len(dict_by_state)>0:
    dict_by_date[last_date] = dict_by_state
    date_list.append(last_date)

datums = []
for key in col_d:
    datums.append(col_d[key])

with open('brazil-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in datums:
            hbuff.append(state+'-'+dat)
    the_file.write(','.join(hbuff)+'\n')

    date_list.sort()
    for date in date_list:
        if date > '2020-02-29':
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
            the_file.write(','.join(buff)+'\n')
    
