# Read RKI data by age from Germany

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

age_groups = {
    'A00-A04':'a0',
    'A05-A14':'a1',
    'A15-A34':'a2',
    'A35-A59':'a3',
    'A60-A79':'a4',
    'A80+':'a5'
}


locations = []
for state in regional_locations:
    locations.append(regional_locations[state])

pt_by_state = {}
dt_by_state = {}
dicts = [pt_by_state, dt_by_state]
files = ['truth_RKI-Cumulative Cases by Age_Germany.csv','truth_RKI-Cumulative Deaths by Age_Germany.csv']

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
                    if location in locations:
                        age_group = fields[3]
                        if age_group in age_groups:
                            value = fields[4].strip()
                            location_age = '_'.join([location,age_groups[age_group]])
                            if location_age in dict:
                                dict[location_age][date] = value
                            else:
                                dict[location_age] = {date:value}
                if (date - end_date).days > 0:
                    end_date = date

start_date = datetime.date(2020, 3, 1)
with open('germany-rki-age-pypm.csv', 'w') as the_file:

    ndays = (end_date - start_date).days + 1
    for i in range(ndays):
        date = start_date + datetime.timedelta(days=i)

    hbuff = ['date']
    for state in regional_locations:
        abbrev = regional_abbreviations[state]
        for age_group in age_groups:
            abbrev_age = '_'.join([abbrev,age_groups[age_group]])
            for dat in ['pt','dt']:
                hbuff.append(abbrev_age + '-' + dat)
    the_file.write(','.join(hbuff) + '\n')

    ndays = (end_date - start_date).days + 1
    for i in range(ndays):
        date = start_date + datetime.timedelta(days=i)
        buff = [str(date)]
        for state in regional_locations:
            location = regional_locations[state]
            for age_group in age_groups:
                location_age = '_'.join([location, age_groups[age_group]])
                if date in pt_by_state[location_age]:
                    buff.append(pt_by_state[location_age][date])
                else:
                    buff.append('')
                if location_age in dt_by_state and date in dt_by_state[location_age]:
                    buff.append(dt_by_state[location_age][date])
                else:
                    buff.append('')

        the_file.write(','.join(buff) + '\n')
