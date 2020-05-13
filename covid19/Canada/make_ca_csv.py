# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:08:22 2020

@author: karlen
"""
import datetime

d_d={'TotalCases':['pt'],
'TotalDeaths':['dt'],
'DailyDeaths':['dd'],
'TotalHospitalized':['ht'],
'DailyHospitalized':['hd'],
'TotalICU':['it'],
'DailyICU':['id']
}

col_d ={}

provs = ['AB','BC','MB','NB','NL','NS','NT','NU','ON','PE','QC','SK','YT']

i=0

last_date = datetime.date(2000,1,1)
col_d = {}
dict_by_date = {}
dict_by_prov = {}
date_list = []
with open('Provincial_Daily_Totals.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        if i == 0:
            j=0
            for col in cols:
                if col in d_d:
                    col_d[j]=d_d[col][0]
                j+=1
        else:
            prov = cols[3]
            if prov in provs:
                dt = cols[0].split(' ')
                dd = dt[0].split('/')
                date = datetime.date(int(dd[0]),int(dd[1]),int(dd[2]))
                # date = datetime.datetime.fromtimestamp(date_ms/1000.0).date()
                if date != last_date and last_date != datetime.date(2000,1,1):
                    dict_by_date[last_date] = dict_by_prov
                    date_list.append(last_date)
                    dict_by_prov = {}
    
                dict_by_datum = {}
                for i_col in col_d:
                    dict_by_datum[col_d[i_col]] = str(cols[i_col])
                dict_by_prov[prov] = dict_by_datum
                last_date = date
        i+=1

if len(dict_by_prov) > 0:
    dict_by_date[last_date] = dict_by_prov
    date_list.append(last_date)

datums = []
for key in col_d:
    datums.append(col_d[key])

start_date = datetime.date(2020, 3, 1)
with open('ca-pypm.csv', 'w') as the_file:
#    the_file.write('Hello\n')

    hbuff = ['date']
    for prov in provs:
        for dat in datums:
            hbuff.append(prov+'-'+dat)
    the_file.write(','.join(hbuff)+'\n')


    date_list.sort()
    for date in date_list:
        if date >= start_date:
            dict_by_prov = dict_by_date[date]
            buff = [str(date)]
            for prov in provs:
                dict_by_datum = None
                if prov in dict_by_prov:
                    dict_by_datum = dict_by_prov[prov]
                for dat in datums:
                    val = ''
                    if dict_by_datum is not None:
                        val = dict_by_datum[dat]
                    buff.append(val)
            the_file.write(','.join(buff)+'\n')
    