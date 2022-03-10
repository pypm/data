# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data provided by US covidtracking.com, JHU, HHS, CDC
    """
    data = {}
    data['nation'] = 'USA'
    data['description'] = 'US by state'
    data['source'] = 'Covid tracking US, JHU CSSE, US HHS, US CDC, New York Times'
    data['source_url'] = 'https://covidtracking.com and https://github.com/CSSEGISandData/COVID-19'\
                         ' and https://healthdata.gov/dataset/'\
                         'covid-19-reported-patient-impact-and-hospital-capacity-state-timeseries'\
                         ' and https://data.cdc.gov/Laboratory-Surveillance/Nationwide-Commercial-Laboratory' \
                         '-Seroprevalence-Su/d2tw-32xv'\
                         ' and https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'\
                         ' and https://data.cdc.gov/Vaccinations/COVID-19-Vaccination-Trends-in-the-United-States-N/rh2h-3yt2'

    # common regional abbreviations used in the data files
    regional_abbreviations = {
        'Alaska':'AK',
        'Alabama':'AL',
        'Arkansas':'AR',
        'American Samoa':'AS',
        'Arizona':'AZ',
        'California':'CA',
        'Colorado':'CO',
        'Connecticut':'CT',
        'District Of Columbia':'DC',
        'Delaware':'DE',
        'Florida':'FL',
        'Georgia':'GA',
        'Guam':'GU',
        'Hawaii':'HI',
        'Iowa':'IA',
        'Idaho':'ID',
        'Illinois':'IL',
        'Indiana':'IN',
        'Kansas':'KS',
        'Kentucky':'KY',
        'Louisiana':'LA',
        'Massachusetts':'MA',
        'Maryland':'MD',
        'Maine':'ME',
        'Michigan':'MI',
        'Minnesota':'MN',
        'Missouri':'MO',
        'Northern Mariana Islands':'MP',
        'Mississippi':'MS',
        'Montana':'MT',
        'North Carolina':'NC',
        'North Dakota':'ND',
        'Nebraska':'NE',
        'New Hampshire':'NH',
        'New Jersey':'NJ',
        'New Mexico':'NM',
        'Nevada':'NV',
        'New York':'NY',
        'Ohio':'OH',
        'Oklahoma':'OK',
        'Oregon':'OR',
        'Pennsylvania':'PA',
        'Puerto Rico':'PR',
        'Rhode Island':'RI',
        'South Carolina':'SC',
        'South Dakota':'SD',
        'Tennessee':'TN',
        'Texas':'TX',
        'Utah':'UT',
        'Virginia':'VA',
        'US Virgin Islands':'VI',
        'Vermont':'VT',
        'Washington':'WA',
        'Wisconsin':'WI',
        'West Virginia':'WV',
        'Wyoming':'WY'
        }

    files_data = {}
    # switch from jhu to nyt on Dec 27, 2021
    filenames = ['usa-pypm.csv','usa-nyt-pypm.csv','usa-hhs-pypm.csv','usa-cdc-pypm.csv','usa-vacc-pypm.csv',
                 'usa-jhu-pypm.csv',]
    sources = ['covidtracking.com','New York Times','US HHS','US CDC','US CDC','JHU']
    for i,filename in enumerate(filenames):
        file_data = {}
        file_data['source'] = sources[i]
        file_data['date header'] = 'Date'
        file_data['date start'] = [2020, 3, 1]

        files_data[filename] = file_data
    data['files'] = files_data

    #for each region, define location of each population data (file/column header)
    #either daily or total (or both) data can be provided

    regions_data = {}
    # prior to including HHS data:
    #f0_populations = ['hospitalized', 'in_hospital',
    #                  'icu admissions', 'in_icu',
    #                  'ventilated', 'on_ventilator']
    f0_populations = ['icu admissions',
                      'ventilated', 'on_ventilator']
    f1_populations = ['reported', 'deaths']
    f2_populations = ['in_icu','hospitalized','in_hospital']
    f3_populations = ['sero_positive']
    f4_populations = ['vaccinated','boosted']

    for region in regional_abbreviations:

        populations_data = {}

        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = regional_abbreviations[region]+'-pt'
            if population == 'deaths':
                header = regional_abbreviations[region]+'-dt'
            if population == 'hospitalized':
                header = regional_abbreviations[region]+'-ht'
            if population == 'in_hospital':
                header = regional_abbreviations[region]+'-hc'
            if population == 'icu admissions':
                header = regional_abbreviations[region]+'-it'
            if population == 'in_icu':
                header = regional_abbreviations[region]+'-ic'
            if population == 'ventilated':
                header = regional_abbreviations[region]+'-vt'
            if population == 'on_ventilator':
                header = regional_abbreviations[region]+'-vc'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        filename = filenames[1]
        for population in f1_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = regional_abbreviations[region]+'-pt'
            if population == 'deaths':
                header = regional_abbreviations[region]+'-dt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        filename = filenames[2]
        for population in f2_populations:
            if population in ['in_icu','in_hospital']:
                pop_data_total = {}
                pop_data_total['filename'] = filename
                header = ''
                if population == 'in_icu':
                    header = regional_abbreviations[region]+'-ic'
                if population == 'in_hospital':
                    header = regional_abbreviations[region]+'-hc'

                pop_data_total['header'] = header

                population_data = {'total': pop_data_total}
                populations_data[population] = population_data
            if population in ['hospitalized']:
                pop_data_daily = {}
                pop_data_daily['filename'] = filename
                header = ''
                if population == 'hospitalized':
                    header = regional_abbreviations[region] + '-hd'

                pop_data_daily['header'] = header

                population_data = {'daily': pop_data_daily}
                populations_data[population] = population_data

        filename = filenames[3]
        for population in f3_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'sero_positive':
                header = regional_abbreviations[region] + '-nt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        filename = filenames[4]
        for population in f4_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'vaccinated':
                header = regional_abbreviations[region] + '-xt'
            if population == 'boosted':
                header = regional_abbreviations[region] + '-yt'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[region] = populations_data

    data['regional_data'] = regions_data

    return data
