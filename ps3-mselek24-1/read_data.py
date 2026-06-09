import datetime
import json
from datetime import datetime

def add_daily_record(country_obj, date, cases, deaths):
    """
    Adds a daily record of cases and deaths to the country's data.

    Parameters:
    - country_obj (dict): The country's data object.
    - date (str): The date of the record in DD/MM/YYYY format.
    - cases (int): Number of new cases.
    - deaths (int): Number of new deaths.
    """
    country_obj['daily_records'].append({'date': date, 'cases': cases, 'deaths': deaths})





def add_weekly_case_data(country_obj, age_group, year_week, new_cases):
    """
    Adds a weekly record of new cases for a specific age group to the country's data.

    Parameters:
    - country_obj (dict): The country's data object.
    - age_group (str): The age group for the data record.
    - year_week (str): The week of the year in YYYY-WW format.
    - new_cases (int): Number of new cases.
    """
    country_obj['weekly_records'][age_group].append({'year_week': year_week, 'new_cases': new_cases})





def create_country_entry(name, population):
    """
    Creates a new country entry with the specified name and population,
    including data structures for daily and weekly records.

    Parameters:
    - name (str): Name of the country.
    - population (int): Population of the country.

    Returns:
    dict: A dictionary object representing the country, including placeholders for daily and weekly data.
    """
    return {
        'name': name,
        'population': population,
        'population_by_agegroup': {'<15yr': -1, '15-24yr': -1, '25-49yr': -1, '50-64yr': -1, '65-79yr': -1, '80+yr': -1},
        'daily_records': [],
        'weekly_records': {'<15yr': [], '15-24yr': [], '25-49yr': [], '50-64yr': [], '65-79yr': [], '80+yr': []},
    }








def process_daily_data(db):
    """
    Processes daily COVID-19 case and death data from a JSON file.

    This function reads from a predefined JSON file ('covid_data.json'), extracting
    information about new daily cases and deaths for each country within a specified
    date range. Each country's data is then added or updated in the provided database
    dictionary.

    Parameters:
    - db (dict): The database dictionary where each country's data is stored. Keys are
                 country codes, and values are dictionaries with the country's data.

    Returns:
    None. The function updates the 'db' dictionary in place.
    """
    with open('covid_data.json', 'r') as file:
      data = json.load(file)
      lst = data['records']

      min_d = datetime.strptime('07/03/2021', '%d/%m/%Y')
      max_d = datetime.strptime('03/05/2021', '%d/%m/%Y')

      for d in lst:
          date_string = d['dateRep']
          date_object = datetime.strptime(date_string, '%d/%m/%Y')

          if d["geoId"] not in db:
              db[d["geoId"]] = create_country_entry(d["countriesAndTerritories"],int(d["popData2020"]))

          if date_object > min_d and date_object < max_d:
              add_daily_record(db[d["geoId"]],d['dateRep'],d['cases'],d['deaths'])




def process_weekly_data(db):
    with open('age_cases.json', 'r') as file:
        records = json.load(file)
        for record in records:
            year, week = record['year_week'].split('-')

            year = int(year)
            week = int(week)

            if year == 2021 and 9 < week < 18:
                key = record['country_code']
                age_group = record['age_group']
            
                if key not in db:
                    db[key] = create_country_entry(record['country'], 0)

                if db[key]['population_by_agegroup'][age_group] == -1:
                    db[key]['population_by_agegroup'][age_group] = int(record['population'])

                add_weekly_case_data(db[key],age_group,record['year_week'],record['new_cases'])
    
                
        
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    