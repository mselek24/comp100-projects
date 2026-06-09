from covid_data_analysis import total_cases_and_deaths_per_1m, calc_exposure_per_age_group
import json


def analyze_covid_impact(db):
    """
    Analyzes COVID-19 impact across EU countries from the given dataset.

    Parameters:
    - db (dict): The database containing COVID-19 data for each country.

    Returns:
    tuple: A tuple containing analysis results in the following order:
        - top_death_country (str): The name of the country with the highest number of deaths per 1 million population.
        - top_death_cnt (int): The highest number of deaths per 1 million population across all countries.
        - top_case_country (str): The name of the country with the highest number of cases per 1 million population.
        - top_case_cnt (int): The highest number of cases per 1 million population across all countries.
        - most_exposed_age_group (str): The age group with the highest average exposure (infection rate) across all countries.
        - least_exposed_age_group (str): The age group with the lowest average exposure (infection rate) across all countries.
    """

    top_case_cnt = 0
    top_death_cnt = 0
    top_case_country = ""
    top_death_country = ""
    exposure_sums = {'<15yr': 0,'15-24yr': 0,'25-49yr': 0,'50-64yr': 0,'65-79yr': 0,'80+yr': 0}

    exposure_counts = {'<15yr': 0,'15-24yr': 0,'25-49yr': 0,'50-64yr': 0,'65-79yr': 0,'80+yr': 0}
    for country_code in db:
        country_obj = db[country_code]

        cases_per_1m, deaths_per_1m = total_cases_and_deaths_per_1m(country_obj)

        if cases_per_1m > top_case_cnt:
            top_case_cnt = cases_per_1m
            top_case_country = country_obj['name']

        if deaths_per_1m > top_death_cnt:
            top_death_cnt = deaths_per_1m
            top_death_country = country_obj['name']

        exposure_dict = calc_exposure_per_age_group(country_obj)

        for age_group in exposure_dict:
            if country_obj['population_by_agegroup'][age_group] != -1:
                exposure_sums[age_group] += exposure_dict[age_group]
                exposure_counts[age_group] += 1

    average_exposures = {}
    for age_group in exposure_sums:
        if exposure_counts[age_group] == 0:
            average_exposures[age_group] = 0
        else:
            average_exposures[age_group] = exposure_sums[age_group] / exposure_counts[age_group]

    most_exposed_age_group = ""
    least_exposed_age_group = ""

    max_exposure = -1
    min_exposure = None

    for age_group in average_exposures:
        if average_exposures[age_group] > max_exposure:
            max_exposure = average_exposures[age_group]
            most_exposed_age_group = age_group

        if min_exposure is None or average_exposures[age_group] < min_exposure:
            min_exposure = average_exposures[age_group]
            least_exposed_age_group = age_group
 
    return (top_death_country, top_death_cnt, top_case_country,
            top_case_cnt, most_exposed_age_group, least_exposed_age_group)


def write_summary_to_json(data):
    """
    Writes a summary of COVID-19 impact analysis to a JSON file.

    This function takes a tuple containing data on the highest death and case rates per million,
    along with the most and least exposed age groups, and writes this information to a JSON file.
    The data is structured into a readable format that allows easy access and understanding.

    Parameters:
        data (tuple): A tuple containing the following information in order:
                      - Country with the highest deaths per million (str)
                      - Number of deaths per million in that country (int or float)
                      - Country with the highest cases per million (str)
                      - Number of cases per million in that country (int or float)
                      - Most exposed age group (str)
                      - Least exposed age group (str)

    The function creates a dictionary with this data, which is then written to 'covid_impact_summary.json'
    using a pretty-printed JSON format.

    Example of `data` input:
        ("Italy", 1523, "Czech Republic", 15827, "50-64yr", "<15yr")

    Output:
        A JSON file named 'covid_impact_summary.json' with the structured data.
    """
    summary = {"Highest_Deaths_per_1M": {"Country": data[0],"Deaths_per_1M": data[1]},"Highest_Cases_per_1M": {"Country": data[2],"Cases_per_1M": data[3]},"Most_Exposed_Age_Group": data[4],"Least_Exposed_Age_Group": data[5]}

    with open('covid_impact_summary.json', 'w') as file:
        json.dump(summary, file, indent=4)