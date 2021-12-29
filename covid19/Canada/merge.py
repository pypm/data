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

v_provs = ['ON', 'BC', 'QC', 'AB', 'SK', 'NS', 'MB', 'NB', 'NL', 'PE', 'YT', 'NT', 'NU']
v_datums = [['pd', 'pt'], ['dd', 'dt']]
viri_by_date = {}

i = 0
v_date = datetime.date(2020, 3, 1)
with open('CV-TR.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        if i > 0:
            icol = 1
            viri_dict = {}
            for v_datum in v_datums:
                for v_prov in v_provs:
                    for v_dat in v_datum:
                        viri_dict[v_prov + '-' + v_dat] = cols[icol]
                        icol += 1
            viri_by_date[v_date] = viri_dict
            v_date += datetime.timedelta(days=1)
        i += 1

v_provs2 = ['AB', 'SK', 'BC', 'NS', 'ON', 'MB', 'QC', 'NB', 'NL']
v_datums2 = [['ht', 'it']]
viri_by_date2 = {}

i = 0
v_date = datetime.date(2020, 3, 1)
with open('CV - H.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        if i > 0:
            icol = 1
            viri_dict = {}
            for v_datum in v_datums2:
                for v_prov in v_provs2:
                    for v_dat in v_datum:
                        viri_dict[v_prov + '-' + v_dat] = cols[icol]
                        icol += 1
            viri_by_date2[v_date] = viri_dict
            v_date += datetime.timedelta(days=1)
        i += 1

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
            prov = cols[2]
            if prov in provs:
                dt = cols[4].split(' ')
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

# replace BC data with provincial data source

bc_pd = {}
bc_pt = {}
with open('../BC/bc-pypm.csv') as f:
    for i, line in enumerate(f):
        if i>0:
            date = datetime.date(2020,3,1)+datetime.timedelta(days=i-1)
            bc_pd[date] = line.split(',')[1]
            bc_pt[date] = line.split(',')[2]

for date in date_list:
    if date in dict_by_date and date in bc_pd:
        dict_by_date[date]['BC']['pd'] = bc_pd[date]
        dict_by_date[date]['BC']['pt'] = bc_pt[date]

    if date in viri_by_date and date in bc_pd:
        viri_by_date[date]['BC-pd'] = bc_pd[date]
        viri_by_date[date]['BC-pt'] = bc_pt[date]

# read in any hospital admission data available (BC, Manitoba, Quebec only)

hd_by_prov = {}
id_by_prov = {}

# BC (from Jens)
prov = 'BC'
hd_by_date = {}
prev_date = None
prev_cumul = 0
with open('bc_total_hospitalizations.csv') as f:
    for i, line in enumerate(f):
        if i > 0:
            fields = line.split(',')
            df = fields[0].split(' ')[0].split('-')
            date = datetime.date(int(df[0]), int(df[1]), int(df[2]))
            ha = fields[1]
            if ha == 'BC':
                cumul = int(fields[2])
                new_admissions = cumul - prev_cumul
                if new_admissions > 0:
                    if prev_date is not None:
                        n_day = (date-prev_date).days
                        if n_day == 1:
                            hd_by_date[date] = max(0,new_admissions)
                        else:
                            nominal = int((new_admissions - new_admissions % n_day)/n_day)
                            for i_day in range(n_day):
                                back_day = date - datetime.timedelta(days = i_day)
                                extra = 0
                                if i_day < new_admissions % n_day:
                                    extra = 1
                                hd_by_date[back_day] = nominal + extra

                    prev_date = date
                    prev_cumul = cumul

hd_by_prov[prov] = hd_by_date

# Manitoba - also replace ESRI data by provincial data:
# 'TotalCases': ['pt'], 'TotalDeaths': ['dt'], 'TotalHospitalized': ['ht'], 'TotalICU': ['it']
prov = 'MB'
hd_by_date = {}
id_by_date = {}

cases = {'header':'Cumulative_Cases', 'sym':'pt', 'column':None}
deaths = {'header':'Total_Deaths', 'sym':'dt', 'column':None}
hosp_admin = {'header':'New_IP_Admissions_Total', 'sym':'hd', 'column':None}
hosp_occup = {'header':'Current_Hospitalizations___Tota', 'sym':'ht', 'column':None}
icu_admin = {'header':'New_ICU_Admissions', 'sym':'id', 'column':None}
icu_occup = {'header':'Current_ICU___Total', 'sym':'it', 'column':None}
csv_data = [cases, deaths, hosp_admin, hosp_occup, icu_admin, icu_occup]
date_data = {'header':'Date', 'sym':'', 'column':None}
mb_data = csv_data+[date_data]

with open('Manitoba_COVID-19_–_Daily_Cases_and_Hospitalizations_(historical).csv') as f:
    for i, line in enumerate(f):
        fields = line.split(',')
        if i == 0:
            for i_field, field in enumerate(fields):
                for datum in mb_data:
                    if datum['header'] == field:
                        datum['column'] = i_field
                        break
        else:
            raw_datetime = fields[date_data['column']]
            raw_date = raw_datetime.split(' ')[0]
            dd = raw_date.split('/')
            if len(dd) == 3:
                date = datetime.date(int(dd[0]), int(dd[1]), int(dd[2]))
                if (date - datetime.date(2020,2,29)).days > 0:
                    for datum in csv_data:
                        sym = datum['sym']
                        value = (fields[datum['column']]).strip()
                        if sym in ['pt', 'dt', 'ht', 'it']:
                            if date in dict_by_date:
                                dict_by_date[date]['MB'][sym] = value

                            if date in viri_by_date and date in bc_pd:
                                viri_by_date[date]['MB-'+sym] = value

                        elif sym == 'hd':
                            hd_by_date[date] = value
                        elif sym == 'id':
                            id_by_date[date] = value

hd_by_prov[prov] = hd_by_date
id_by_prov[prov] = id_by_date

# Quebec
prov = 'QC'
hd_by_date = {}
id_by_date = {}
with open('graph_3-2_page_principale.csv') as f:
    for i, line in enumerate(f):
        if i > 0:
            fields = line.split(',')
            df = fields[0].split(' ')[0].split('-')
            date = datetime.date(int(df[0][1:]), int(df[1]), int(df[2]))
            nih = int(fields[1])
            icu = int(fields[2])
            hd_by_date[date] = nih+icu
            id_by_date[date] = icu
hd_by_prov[prov] = hd_by_date
id_by_prov[prov] = id_by_date

start_date = datetime.date(2020, 3, 1)
esri_date = datetime.date(2020, 4, 26)
with open('ca-pypm.csv', 'w') as the_file:
    #    the_file.write('Hello\n')

    hbuff = ['date']
    for prov in provs:
        hbuff.append(prov + '-pd')
        for dat in datums:
            hbuff.append(prov + '-' + dat)
    for prov in provs:
        for dat in ['hd','id']:
            hbuff.append(prov + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    date_list.sort()
    last_dict_by_prov = {}
    for date in date_list:
        dict_by_prov = dict_by_date[date]
        if date >= start_date:
            buff = [str(date)]
            if (date - esri_date).days >= 0:
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
                    dat = 'pd'
                    buff.append(viri_by_date[date][prov + '-pd'])
                    for dat in datums:
                        key = prov + '-' + dat
                        if key in viri_by_date[date]:
                            buff.append(viri_by_date[date][key])
                        elif key in viri_by_date2[date]:
                            buff.append(viri_by_date2[date][key])
                        else:
                            buff.append('')
            for prov in provs:
                if prov in hd_by_prov and date in hd_by_prov[prov]:
                    buff.append(str(hd_by_prov[prov][date]))
                else:
                    buff.append('')

                if prov in id_by_prov and date in id_by_prov[prov]:
                    buff.append(str(id_by_prov[prov][date]))
                else:
                    buff.append('')

            the_file.write(','.join(buff) + '\n')
        last_dict_by_prov = dict_by_prov
