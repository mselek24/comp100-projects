def daily_records_to_string(country_obj, idxs):
    output_str = ""
    for idx in idxs:
        record = country_obj['daily_records'][idx]
        output_str += f"Date: {record['date']}, Cases: {record['cases']}, Deaths: {record['deaths']} \n"

    return output_str


def get_total_cases(country_obj):
    total_cases = 0
    for record in country_obj['daily_records']:
        total_cases += int(record['cases'])

    return total_cases


def get_total_deaths(country_obj):
    total_deaths = 0

    for record in country_obj['daily_records']:
        total_deaths += int(record['deaths'])

    return total_deaths


def total_cases_and_deaths_per_1m(country_obj):
    total_cases = get_total_cases(country_obj)
    total_deaths = get_total_deaths(country_obj)

    population = int(country_obj['population'])

    if population == 0:
        return 0, 0

    cases_per_1m = total_cases / population * 1000000
    deaths_per_1m = total_deaths / population * 1000000


    return int(cases_per_1m), int(deaths_per_1m)


def sort_records_by(country_obj, param):
    """
    Sorts daily records by either cases or deaths and returns the indices of the sorted records.
    """
    nums = [(i, record[param]) for i, record in enumerate(country_obj['daily_records'])]

    nums.sort(key=lambda x: x[1])

    indexes = []

    for item in nums:
        indexes.append(item[0])

    return indexes


def find_top_k_cases(country_obj, k):
    idxs = sort_records_by(country_obj, "cases")[-k:]
    out = daily_records_to_string(country_obj, idxs)

    return out


def find_top_k_deaths(country_obj, k):
    idxs = sort_records_by(country_obj, "deaths")[-k:]
    out = daily_records_to_string(country_obj, idxs)

    return out


def calc_exposure_per_age_group(country_obj):
    exposure_dict = {}

    for age_group in country_obj['weekly_records']:
        t_cases = 0

        for record in country_obj['weekly_records'][age_group]:
            t_cases += int(record['new_cases'])

        population = country_obj['population_by_agegroup'][age_group]

        if population == -1 or population == 0:
            exposure_dict[age_group] = 0
        else:
            exposure_dict[age_group] = t_cases / population


    return exposure_dict


def find_most_exposed_age_group(country_obj):
    exposure_dict = calc_exposure_per_age_group(country_obj)
    the_group = ""
    max_exposure = -11

    for age_group in exposure_dict:
        if exposure_dict[age_group] > max_exposure:
            max_exposure = exposure_dict[age_group]
            the_group = age_group
    return the_group


def find_least_exposed_age_group(country_obj):
    exposure_dict = calc_exposure_per_age_group(country_obj)

    the_group = ""
    min_exposure = 0

    for age_group in exposure_dict:
        if min_exposure== 0 or exposure_dict[age_group] < min_exposure:
            min_exposure = exposure_dict[age_group]
            the_group = age_group


    return the_group


def calc_prob_of_cases_per_age_group(country_obj):
    case = {}
    total_cases = 0

    for age_group in country_obj['weekly_records']:
        age_group_cases = 0

        for record in country_obj['weekly_records'][age_group]:
            age_group_cases += int(record['new_cases'])

        case[age_group] = age_group_cases
        total_cases += age_group_cases

    prob_dict = {}

    for age_group in case:
        if total_cases == 0:
            prob_dict[age_group] = 0
        else:
            prob_dict[age_group] = case[age_group] / total_cases


    return prob_dict


def distribute_deaths_to_age_groups(country_obj):
    """
    Distributes the total number of deaths across age groups based on the probability of cases per age group
    and normalized weighting of probability of deaths.
    """
    case_probs = calc_prob_of_cases_per_age_group(country_obj)
    age_groups = list(case_probs.keys())
    death_probs = {
        '<15yr': 0.05,
        '15-24yr': 0.05,
        '25-49yr': 0.1,
        '50-64yr': 0.2,
        '65-79yr': 0.25,
        '80+yr': 0.35
    }

    weighted_probs = {}

    for age_group in age_groups:
        weighted_probs[age_group] = case_probs[age_group] * death_probs[age_group]

    total_weight = 0

    for age_group in age_groups:
        total_weight += weighted_probs[age_group]

    total_deaths = get_total_deaths(country_obj)

    death_distribution = {}

    for age_group in age_groups:
        if total_weight == 0:
            death_distribution[age_group] = 0
        else:
            normalized_prob = weighted_probs[age_group] / total_weight
            death_distribution[age_group] = normalized_prob * total_deaths


    return total_deaths, death_distribution