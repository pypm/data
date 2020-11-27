# Read DIVI data from Germany

import numpy as np
import datetime
from datetime import timedelta

regional_abbreviations = {
        'Baden-Wurttemberg':'bw',
        'Bavaria':'by',
        'Berlin':'be',
        'Brandenburg':'bb',
        'Bremen':'hb',
        'Hamburg':'hh',
        'Hesse':'he',
        'Lower Saxony':'ni',
        'Mecklenburg-Vorpommern':'mv',
        'North Rhine-Westphalia':'nw',
        'Rhineland-Palatinate':'rp',
        'Saarland':'sl',
        'Saxony':'sn',
        'Saxony-Anhalt':'st',
        'Schleswig-Holstein':'sh',
        'Thuringia':'th',
        'Germany':'de'
    }

regional_locations = {
        'Baden-Wurttemberg':'GM01',
        'Bavaria':'GM02',
        'Bremen':'GM03',
        'Hamburg':'GM04',
        'Hesse':'GM05',
        'Lower Saxony':'GM06',
        'North Rhine-Westphalia':'GM07',
        'Rhineland-Palatinate':'GM08',
        'Saarland':'GM09',
        'Schleswig-Holstein':'GM10',
        'Brandenburg':'GM11',
        'Mecklenburg-Vorpommern':'GM12',
        'Saxony':'GM13',
        'Saxony-Anhalt':'GM14',
        'Thuringia':'GM15',
        'Berlin':'GM16',
        'Germany':'GM'
    }

ic_by_state = {}
vc_by_state = {}
dicts = [ic_by_state, vc_by_state]
files = ['truth_DIVI-Current ICU_Germany.csv','truth_DIVI-Current Ventilated_Germany.csv']

end_date = datetime.date(2020, 3, 1)
for i, file in enumerate(files):
    dict = dicts[i]
    with open(file) as f:
        for line in f:
            fields = line.split(',')
            dd = fields[0].split('-')
            if len(dd) == 3:
                date = datetime.date(int(dd[0]), int(dd[1]), int(dd[2]))
                if (date - datetime.date(2020,2,29)).days > 0:
                    location = fields[1]
                    value = fields[3].strip()
                    if location in dict:
                        dict[location][date] = value
                    else:
                        dict[location] = {date:value}
                if (date - end_date).days > 0:
                    end_date = date

start_date = datetime.date(2020, 3, 1)
with open('germany-divi-pypm.csv', 'w') as the_file:

    ndays = (end_date - start_date).days + 1
    for i in range(ndays):
        date = start_date + datetime.timedelta(days=i)

    hbuff = ['date']
    for state in regional_locations:
        abbrev = regional_abbreviations[state]
        for dat in ['ic','vc']:
            hbuff.append(abbrev + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    ndays = (end_date - start_date).days + 1
    for i in range(ndays):
        date = start_date + datetime.timedelta(days=i)
        buff = [str(date)]
        for state in regional_locations:
            location = regional_locations[state]
            if date in ic_by_state[location]:
                buff.append(ic_by_state[location][date])
            else:
                buff.append('')
            if date in vc_by_state[location]:
                buff.append(vc_by_state[location][date])
            else:
                buff.append('')

        the_file.write(','.join(buff) + '\n')
