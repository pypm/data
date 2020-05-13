# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:08:22 2020

@author: karlen
"""
import datetime

last_date = datetime.date(2000, 1, 1)

dict_by_category = {}
ha_categories = []
fixed_categories = ['All', 'Male', 'Female']
age_categories = []
cumul_by_category = {}

def add_entry(date, category):
    if category not in dict_by_category:
        dict_by_category[category] = {date: 1}
    else:
        if date in dict_by_category[category]:
            dict_by_category[category][date] += 1
        else:
            dict_by_category[category][date] = 1


def get_data(date, category):
    if category not in cumul_by_category:
        cumul_by_category[category] = 0
    today = 0
    if date in dict_by_category[category]:
        today = dict_by_category[category][date]
        cumul_by_category[category] += today
    return today, cumul_by_category[category]


first_date = None
i = 0
with open('BCCDC_COVID19_Dashboard_Case_Details.csv') as f:
    for line in f:
        cols = line.strip().split(',')
        for j in range(len(cols)):
            cols[j] = cols[j].strip('"')
        if i > 0:
            dd = cols[0].split('-')
            date = datetime.date(int(dd[0]), int(dd[1]), int(dd[2]))
            if i == 1:
                first_date = date

            add_entry(date, 'All')
            add_entry(date, cols[1])
            if cols[1] not in ha_categories:
                ha_categories.append(cols[1].strip('"'))
            if cols[2] == 'M':
                add_entry(date, 'Male')
            else:
                add_entry(date, 'Female')
            add_entry(date, cols[3])
            if cols[3] not in age_categories:
                age_categories.append(cols[3])

            last_date = date
        i += 1

ha_categories.sort()
all_categories = fixed_categories + ha_categories + age_categories

start_date = datetime.date(2020, 3, 1)
with open('bc-pypm.csv', 'w') as the_file:

    ndays = (start_date - first_date).days
    for i in range(ndays):
        date = first_date + datetime.timedelta(days=i)
        for category in all_categories:
            daily, total = get_data(date, category)

    hbuff = ['date']
    for category in all_categories:
        for dat in ['pd','pt']:
            hbuff.append(category + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    ndays = (last_date - start_date).days
    for i in range(ndays):
        date = start_date + datetime.timedelta(days=i)
        buff = [str(date)]
        for category in all_categories:
            daily, total = get_data(date, category)
            buff.append(str(daily))
            buff.append(str(total))

        the_file.write(','.join(buff) + '\n')
