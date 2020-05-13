# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:08:22 2020

@author: karlen
"""

d_d={'positive':['pt','Total cumulative positive test results.'],
'hospitalizedCurrently':['hc','Number of individuals currently hospitalized.'],
'hospitalizedCumulative':['ht','Total number of individuals that have been hospitalized, including those that have been discharged.'],
'inIcuCurrently':['ic','Number of individuals currently in an ICU.'],
'inIcuCumulative':['it','Total number of individuals that have been in the ICU.'],
'onVentilatorCurrently':['vc','Number of individuals currently on a ventilator.'],
'onVentilatorCumulative':['vt','Total number of individuals that have been on a ventilator.'],
'death':['dt','Total cumulative number of people that have died.']}
col_d ={}

states = ['AK','AL','AR','AS','AZ','CA','CO','CT','DC','DE','FL','GA','GU','HI','IA','ID','IL','IN','KS',
          'KY','LA','MA','MD','ME','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY',
          'OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VA','VI','VT','WA','WI','WV','WY']

i=0

last_date = 0
col_d = {}
dict_by_date = {}
dict_by_state = {}
date_list = []
with open('daily.csv') as f:
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
            state = cols[1]
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

with open('usa-pypm.csv', 'w') as the_file:
#    the_file.write('Hello\n')

    hbuff = ['date']
    for state in states:
        for dat in datums:
            hbuff.append(state+'-'+dat)
    the_file.write(','.join(hbuff)+'\n')


    date_list.sort()
    for date in date_list:
        if int(date) > 20200300:
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
    
