# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:08:22 2020

@author: karlen
"""
import datetime

d_d = {'TotalCases': ['pt'],
       'TotalDeaths': ['dt'],
       'DailyDeaths': ['dd'],
       'TotalHospitalized': ['ht'],
       'TotalICU': ['it']
       }

col_d = {}

provs = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']

# read in old virihealth data

v_provs = ['ON','BC','QC','AB','SK','NS','MB','NB','NL','PE','YT','NT','NU']
v_datums = [['pd','pt'],['dd','dt']]
viri_by_date = {}

i=0
v_date = datetime.date(2020,3,1)
with open('CV-TR.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        if i>0:
            icol = 1
            viri_dict = {}
            for v_datum in v_datums:
                for v_prov in v_provs:
                    for v_dat in v_datum:
                        viri_dict[v_prov+'-'+v_dat] = cols[icol]
                        icol += 1
            viri_by_date[v_date] = viri_dict
            v_date += datetime.timedelta(days=1)
        i+=1


v_provs2 = ['AB','SK','BC','NS','ON','MB','QC','NB','NL']
v_datums2 = [['ht','it']]
viri_by_date2 = {}

i=0
v_date = datetime.date(2020,3,1)
with open('CV - H.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        if i>0:
            icol = 1
            viri_dict = {}
            for v_datum in v_datums2:
                for v_prov in v_provs2:
                    for v_dat in v_datum:
                        viri_dict[v_prov+'-'+v_dat] = cols[icol]
                        icol += 1
            viri_by_date2[v_date] = viri_dict
            v_date += datetime.timedelta(days=1)
        i+=1

# Read in esri data

i = 0

last_date = datetime.date(2000, 1, 1)
col_d = {}
dict_by_date = {}
dict_by_prov = {}
date_list = []
with open('Provincial_Daily_Totals.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        if i == 0:
            j = 0
            for col in cols:
                if col in d_d:
                    col_d[j] = d_d[col][0]
                j += 1
        else:
            prov = cols[3]
            if prov in provs:
                dt = cols[0].split(' ')
                dd = dt[0].split('/')
                date = datetime.date(int(dd[0]), int(dd[1]), int(dd[2]))
                # date = datetime.datetime.fromtimestamp(date_ms/1000.0).date()
                if date != last_date and last_date != datetime.date(2000, 1, 1):
                    dict_by_date[last_date] = dict_by_prov
                    date_list.append(last_date)
                    dict_by_prov = {}

                dict_by_datum = {}
                for i_col in col_d:
                    dict_by_datum[col_d[i_col]] = str(cols[i_col])
                dict_by_prov[prov] = dict_by_datum
                last_date = date
        i += 1

if len(dict_by_prov) > 0:
    dict_by_date[last_date] = dict_by_prov
    date_list.append(last_date)

datums = []
for key in col_d:
    datums.append(col_d[key])

start_date = datetime.date(2020, 3, 1)
esri_date = datetime.date(2020,4,26)
with open('ca-pypm.csv', 'w') as the_file:
    #    the_file.write('Hello\n')

    hbuff = ['date']
    for prov in provs:
        hbuff.append(prov+'-pd')
        for dat in datums:
            hbuff.append(prov + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    date_list.sort()
    last_dict_by_prov = {}
    for date in date_list:
        dict_by_prov = dict_by_date[date]
        if date >= start_date:
            buff = [str(date)]
            if (date-esri_date).days >= 0:
                for prov in provs:
                    dict_by_datum = None
                    pd_val = ''
                    if prov in dict_by_prov:
                        dict_by_datum = dict_by_prov[prov]
                        last_dict_by_datum = last_dict_by_prov[prov]
                        if last_dict_by_datum is not None:
                            pd_val = int(dict_by_datum['pt']) - int(last_dict_by_datum['pt'])
                    buff.append(str(pd_val))
                    for dat in datums:
                        val = ''
                        if dict_by_datum is not None:
                            val = dict_by_datum[dat]
                        buff.append(val)
            else:
                for prov in provs:
                    dat='pd'
                    buff.append(viri_by_date[date][prov+'-pd'])
                    for dat in datums:
                        key = prov+'-'+dat
                        if key in viri_by_date[date]:
                            buff.append(viri_by_date[date][key])
                        elif key in viri_by_date2[date]:
                            buff.append(viri_by_date2[date][key])
                        else:
                            buff.append('')
            the_file.write(','.join(buff) + '\n')
        last_dict_by_prov = dict_by_prov
