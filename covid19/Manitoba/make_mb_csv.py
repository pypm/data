# Read MB data

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

cases = {'header':'Cumulative_Cases', 'sym':'pt', 'dict_by_RHA': {}, 'column':None}
deaths = {'header':'Deaths', 'sym':'dt', 'dict_by_RHA': {}, 'column':None}
csv_data = [cases, deaths]

# due to extra characters at the beginning of the file, the Date header does not match - hard code it here
date_data = {'header':'Date', 'sym':'', 'column':0}
rha_data = {'header':'RHA', 'sym':'', 'column':None}
data = csv_data+[date_data,rha_data]

file = 'Manitoba_COVID-19_–_Daily_Cases_by_Status_and_RHA.csv'

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
                    rha = regional_abbreviations[fields[rha_data['column']]]
                    for datum in csv_data:
                        dict_by_RHA = datum['dict_by_RHA']
                        value = (fields[datum['column']]).strip()
                        if rha in dict_by_RHA:
                            dict_by_RHA[rha][date] = value
                        else:
                            dict_by_RHA[rha] = {date:value}

                if (date - end_date).days > 0:
                    end_date = date

start_date = datetime.date(2020, 3, 1)
with open('mb-pypm.csv', 'w') as the_file:

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
            for datum in csv_data:
                dict_by_RHA = datum['dict_by_RHA']
                if date in dict_by_RHA[rha]:
                    buff.append(dict_by_RHA[rha][date])
                else:
                    buff.append('')

        the_file.write(','.join(buff) + '\n')
