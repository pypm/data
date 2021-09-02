# Read MB vaccination data

import numpy as np
import datetime
from datetime import timedelta

regional_abbreviations = {
    'All':'mb',
    'Interlake-Eastern':'ie',
    'Northern':'no',
    'Prairie Mountain Health':'pm',
    'Southern Health-SantÃ© Sud':'sh',
    'Winnipeg':'wg'
    }

first_doses = {'header':'Cumulative_First_Doses', 'sym':'xt', 'dict_by_date': {}, 'column':None}
csv_data = [first_doses]

date_data = {'header':'Vaccination_Date', 'sym':'', 'column':None}
data = csv_data+[date_data]

file = 'Manitoba_COVID-19_Vaccinations_-_Daily_Statistics.csv'

end_date = datetime.date(2020, 3, 1)

with open(file) as f:
    for i,line in enumerate(f):
        fields = line.split(',')
        if i == 0:
            for i_field,field in enumerate(fields):
                for datum in data:
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
                        dict_by_date = datum['dict_by_date']
                        value = (fields[datum['column']]).strip()
                        dict_by_date[date] = value

                if (date - end_date).days > 0:
                    end_date = date

start_date = datetime.date(2020, 3, 1)
with open('mb-vacc-pypm.csv', 'w') as the_file:

    hbuff = ['date']
    for rha_name in regional_abbreviations:
        rha = regional_abbreviations[rha_name]
        for datum in csv_data:
            hbuff.append(rha + '-' + datum['sym'])
    the_file.write(','.join(hbuff) + '\n')

    ndays = (end_date - start_date).days + 1
    for i in range(ndays):
        date = start_date + datetime.timedelta(days=i)
        buff = [str(date)]
        for rha_name in regional_abbreviations:
            rha = regional_abbreviations[rha_name]
            if rha == 'mb':
                for datum in csv_data:
                    dict_by_date = datum['dict_by_date']
                    if date in dict_by_date:
                        buff.append(dict_by_date[date])
                    else:
                        buff.append('')
            else:
                buff.append('')

        the_file.write(','.join(buff) + '\n')
