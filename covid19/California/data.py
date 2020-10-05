# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

# -*- coding: utf-8 -*-
"""
Example of data description file: data.py

@author: karlen
"""

def get_data_description():
    """ Define data provided by BC CDC
    """
    data = {}
    data['nation'] = 'California'
    data['description'] = 'California cases and deaths by age (and hospitalizations)'
    data['source'] = 'California open data portal (and CDC)'
    data['source_url'] = 'https://data.ca.gov/dataset/covid-19-cases and https://gis.cdc.gov/grasp/COVIDNet/COVID19_3.html'

    # categories
    categories = ['0-17','18-49','50-64','65+']

    files_data = {}
    filenames = ['california-pypm.csv']
    for filename in filenames:
        file_data = {}
        file_data['source'] = 'More detailed information if folder has multiple sources'
        file_data['date header'] = 'Date'
        file_data['date start'] = [2020, 3, 1]

        files_data[filename] = file_data
    data['files'] = files_data

    #for each region, define location of each population data (file/column header)
    #either daily or total (or both) data can be provided

    regions_data = {}
    for category in categories:

        populations_data = {}
        f0_populations = ['reported','deaths','hospitalized']
        filename = filenames[0]
        for population in f0_populations:
            pop_data_total = {}
            pop_data_total['filename'] = filename
            header = ''
            if population == 'reported':
                header = category+'-pt'
            if population == 'deaths':
                header = category+'-dt'
            if population == 'hospitalized':
                header = category+'-ht'

            pop_data_total['header'] = header

            population_data = {'total': pop_data_total}
            populations_data[population] = population_data

        regions_data[category] = populations_data

    data['regional_data'] = regions_data

    return data
