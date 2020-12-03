# -*- coding: utf-8 -*-
"""
Read new hospitalization data

@author: karlen
"""

fields = {
    'state': {'label': 'state', 'desc': ' The two digit state code', 'column':0},
    'date': {'label': 'date'},
    'hcx': {'label': 'inpatient_beds_used_covid',
            'desc': 'Reported patients currently hospitalized in an inpatient bed who have suspected or confirmed '
                    'COVID-19 in this state'},
    'hd0': {'label': 'previous_day_admission_adult_covid_confirmed',
            'desc': 'Number of patients who were admitted to an adult inpatient bed on the previous calendar day who '
                    'had confirmed COVID-19 at the time of admission in this state'},
    'hd1': {'label': 'previous_day_admission_pediatric_covid_confirmed',
            'desc': 'Number of pediatric patients who were admitted to an inpatient bed, including NICU, PICU,'
                    ' newborn, and nursery, on the previous calendar day who had confirmed COVID-19 at the time '
                    'of admission in this state'},
    'ic': {'label': 'staffed_icu_adult_patients_confirmed_covid',
           'desc': 'Reported patients currently hospitalized in an adult ICU bed who have confirmed COVID-19 '
                   'in this state'},
    'hc0': {'label': 'total_adult_patients_hospitalized_confirmed_covid',
            'desc': 'Reported patients currently hospitalized in an adult inpatient bed who have laboratory-confirmed '
                    'COVID-19. This include those in observation beds.'},
    'hc1': {'label': 'total_pediatric_patients_hospitalized_confirmed_covid',
            'desc': 'Reported patients currently hospitalized in a pediatric inpatient bed, including NICU, newborn, '
                    'and nursery, who are laboratory-confirmed-positive for COVID-19. This include those in '
                    'observation beds'}
}

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN',
          'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI',
          'WV', 'WY']

i = 0
last_date = 0
col_d = {}
dict_by_date = {}
date_list = []

with open('reported_hospital_utilization_timeseries.csv') as f:
    for line in f:
        columns = line.split(',')
        if i == 0:
            j = 0
            for column in columns:
                for field in fields:
                    if column == fields[field]['label']:
                        fields[field]['column'] = j
                j += 1
        else:
            date = columns[fields['date']['column']]
            if date not in dict_by_date:
                dict_by_date[date] = {}
                date_list.append(date)

            state = columns[fields['state']['column']]

            ic = ''
            try:
                ic = str(columns[fields['ic']['column']])
            except:
                pass
            hd = ''
            try:
                hd = str(int(columns[fields['hd0']['column']])+int(columns[fields['hd1']['column']]))
            except:
                pass
            hc = ''
            try:
                hc = str(int(columns[fields['hc0']['column']]) + int(columns[fields['hc1']['column']]))
            except:
                pass

            dict_by_date[date][state] = {
                'ic': ic,
                'hd': hd,
                'hc': hc
            }

        i += 1

datums = ['ic','hd','hc']

with open('usa-hhs-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for state in states:
        for dat in datums:
            hbuff.append(state + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    date_list.sort()
    for date in date_list:
        if date > '2020-03-00':
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
            the_file.write(','.join(buff) + '\n')
