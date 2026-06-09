import json
import os
import unittest
from datetime import datetime

from covid_data_analysis import (
    distribute_deaths_to_age_groups,
    find_least_exposed_age_group,
    find_most_exposed_age_group,
    find_top_k_cases,
    find_top_k_deaths,
    get_total_cases,
    get_total_deaths,
    total_cases_and_deaths_per_1m,
)
from covid_impact import analyze_covid_impact, write_summary_to_json
from read_data import process_daily_data, process_weekly_data


class TestReadDataAgainstPS03Spec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = {}
        process_daily_data(cls.db)
        process_weekly_data(cls.db)

    def test_q1_daily_keys_and_country_creation(self):
        self.assertIn("AT", self.db)
        self.assertIn("daily_records", self.db["AT"])

    def test_q1_daily_date_range_is_exclusive(self):
        lower_bound = datetime(2021, 3, 7)
        upper_bound = datetime(2021, 5, 3)
        for country in self.db.values():
            for record in country["daily_records"]:
                date_obj = datetime.strptime(record["date"], "%d/%m/%Y")
                self.assertGreater(date_obj, lower_bound)
                self.assertLess(date_obj, upper_bound)

    def test_q2_weekly_keys_and_age_groups(self):
        self.assertIn("AT", self.db)
        weekly = self.db["AT"]["weekly_records"]
        expected_groups = {"<15yr", "15-24yr", "25-49yr", "50-64yr", "65-79yr", "80+yr"}
        self.assertEqual(set(weekly.keys()), expected_groups)

    def test_q2_week_range_is_exclusive(self):
        for country in self.db.values():
            for age_group_records in country["weekly_records"].values():
                for record in age_group_records:
                    year, week = record["year_week"].split("-")
                    self.assertEqual(year, "2021")
                    self.assertGreater(int(week), 9)
                    self.assertLess(int(week), 18)

    def test_q2_population_by_age_group_is_updated(self):
        austria_age_pops = self.db["AT"]["population_by_agegroup"]
        self.assertTrue(all(pop != -1 for pop in austria_age_pops.values()))


class TestCovidDataAnalysisFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.country = {
            "name": "Testland",
            "population": 1_000_000,
            "daily_records": [
                {"date": "01/04/2021", "cases": 100, "deaths": 1},
                {"date": "02/04/2021", "cases": 200, "deaths": 2},
                {"date": "03/04/2021", "cases": 150, "deaths": 3},
            ],
            "weekly_records": {
                "<15yr": [{"new_cases": 50}, {"new_cases": 75}],
                "15-24yr": [{"new_cases": 100}, {"new_cases": 150}],
                "25-49yr": [{"new_cases": 150}, {"new_cases": 100}],
                "50-64yr": [{"new_cases": 50}, {"new_cases": 25}],
                "65-79yr": [{"new_cases": 25}, {"new_cases": 15}],
                "80+yr": [{"new_cases": 10}, {"new_cases": 5}],
            },
            "population_by_agegroup": {
                "<15yr": 200000,
                "15-24yr": 150000,
                "25-49yr": 350000,
                "50-64yr": 200000,
                "65-79yr": 75000,
                "80+yr": 25000,
            },
        }

    def test_q3_total_cases(self):
        self.assertEqual(get_total_cases(self.country), 450)

    def test_q3_total_deaths(self):
        self.assertEqual(get_total_deaths(self.country), 6)

    def test_q3_per_1m(self):
        cases_per_1m, deaths_per_1m = total_cases_and_deaths_per_1m(self.country)
        self.assertEqual(cases_per_1m, 450)
        self.assertEqual(deaths_per_1m, 6)

    def test_q4_most_and_least_exposed_age_group(self):
        self.assertEqual(find_most_exposed_age_group(self.country), "15-24yr")
        self.assertEqual(find_least_exposed_age_group(self.country), "50-64yr")

    def test_q5_distribute_deaths_to_age_groups(self):
        total_deaths, distribution = distribute_deaths_to_age_groups(self.country)
        self.assertEqual(total_deaths, 6)
        self.assertEqual(set(distribution.keys()), set(self.country["weekly_records"].keys()))
        self.assertAlmostEqual(sum(distribution.values()), total_deaths, places=6)

    def test_q6_top_k_cases_and_deaths(self):
        self.assertIn("02/04/2021", find_top_k_cases(self.country, 1))
        self.assertIn("03/04/2021", find_top_k_deaths(self.country, 1))


class TestCovidImpactOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = {}
        process_daily_data(cls.db)
        process_weekly_data(cls.db)

    def test_q7_analyze_returns_6_items(self):
        result = analyze_covid_impact(self.db)
        self.assertEqual(len(result), 6)

    def test_q7_write_summary_json_shape(self):
        result = analyze_covid_impact(self.db)
        write_summary_to_json(result)
        output_path = "covid_impact_summary.json"
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r") as file:
            data = json.load(file)

        self.assertIn("Highest_Deaths_per_1M", data)
        self.assertIn("Highest_Cases_per_1M", data)
        self.assertIn("Most_Exposed_Age_Group", data)
        self.assertIn("Least_Exposed_Age_Group", data)
        self.assertIn("Country", data["Highest_Deaths_per_1M"])
        self.assertIn("Deaths_per_1M", data["Highest_Deaths_per_1M"])
        self.assertIn("Country", data["Highest_Cases_per_1M"])
        self.assertIn("Cases_per_1M", data["Highest_Cases_per_1M"])

        os.remove(output_path)


class TestCovidDataProcessingLegacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = {}
        process_daily_data(cls.db)
        process_weekly_data(cls.db)

    def test_specific_date_cases_and_deaths(self):
        austria_data = self.db["AT"]
        specific_date_record = next(
            (record for record in austria_data["daily_records"] if record["date"] == "01/04/2021"),
            None,
        )
        self.assertIsNotNone(specific_date_record, "Specific date record should not be None")
        self.assertEqual(specific_date_record["cases"], 3107, "Cases do not match expected value")
        self.assertEqual(specific_date_record["deaths"], 28, "Deaths do not match expected value")

    def test_weekly_data_age_group(self):
        austria_data = self.db["AT"]
        week_10_2021_data = austria_data["weekly_records"]["<15yr"]
        self.assertTrue(
            any(record["year_week"] == "2021-10" for record in week_10_2021_data),
            "Weekly data for age group <15yr in week 10 of 2021 should exist",
        )

    def test_population_data_integrity(self):
        austria_data = self.db["AT"]
        self.assertEqual(austria_data["population"], 8901064, "Population does not match expected value")
        self.assertNotEqual(
            austria_data["population_by_agegroup"]["<15yr"],
            -1,
            "Population by age group <15yr should not be -1",
        )

    def test_date_range_inclusion_daily_data(self):
        austria_data = self.db["AT"]
        early_date_record = next(
            (
                record
                for record in austria_data["daily_records"]
                if datetime.strptime(record["date"], "%d/%m/%Y") < datetime(2021, 3, 8)
            ),
            None,
        )
        self.assertIsNone(early_date_record, "Records before 08/03/2021 should not be included")


class TestCountryDataLegacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_country = {
            "name": "Testland",
            "population": 1000000,
            "daily_records": [
                {"date": "2020-01-01", "cases": 100, "deaths": 1},
                {"date": "2020-01-02", "cases": 200, "deaths": 2},
                {"date": "2020-01-03", "cases": 150, "deaths": 3},
            ],
            "weekly_records": {
                "<15yr": [{"new_cases": 50}, {"new_cases": 75}],
                "15-24yr": [{"new_cases": 100}, {"new_cases": 150}],
                "25-49yr": [{"new_cases": 150}, {"new_cases": 100}],
                "50-64yr": [{"new_cases": 50}, {"new_cases": 25}],
                "65-79yr": [{"new_cases": 25}, {"new_cases": 15}],
                "80+yr": [{"new_cases": 10}, {"new_cases": 5}],
            },
            "population_by_agegroup": {
                "<15yr": 200000,
                "15-24yr": 150000,
                "25-49yr": 350000,
                "50-64yr": 200000,
                "65-79yr": 75000,
                "80+yr": 25000,
            },
        }

    def test_get_total_cases(self):
        self.assertEqual(get_total_cases(self.test_country), 450, "Total cases should be 450.")

    def test_get_total_deaths(self):
        self.assertEqual(get_total_deaths(self.test_country), 6, "Total deaths should be 6.")

    def test_total_cases_and_deaths_per_1m(self):
        cases_per_1m, deaths_per_1m = total_cases_and_deaths_per_1m(self.test_country)
        self.assertEqual(cases_per_1m, 450, "Cases per 1 million should be 450.")
        self.assertEqual(deaths_per_1m, 6, "Deaths per 1 million should be 6.")

    def test_find_most_exposed_age_group(self):
        self.assertEqual(
            find_most_exposed_age_group(self.test_country),
            "15-24yr",
            "Most exposed age group should be 15-24yr.",
        )

    def test_find_least_exposed_age_group(self):
        self.assertEqual(
            find_least_exposed_age_group(self.test_country),
            "50-64yr",
            "Least exposed age group should be 50-64yr.",
        )

    def test_distribute_deaths_to_age_groups(self):
        total_deaths, _ = distribute_deaths_to_age_groups(self.test_country)
        self.assertEqual(total_deaths, 6, "Total deaths should be 6.")

    def test_find_top_k_cases(self):
        self.assertIn(
            "2020-01-02",
            find_top_k_cases(self.test_country, 1),
            "Top 1 case date should include 2020-01-02.",
        )

    def test_find_top_k_deaths(self):
        self.assertIn(
            "2020-01-03",
            find_top_k_deaths(self.test_country, 1),
            "Top 1 death date should include 2020-01-03.",
        )


class TestProcessBigDataFixedDatasetLegacy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = {}
        process_daily_data(cls.db)
        process_weekly_data(cls.db)

    def test_with_fixed_dataset(self):
        (
            top_death_country,
            top_death_cnt,
            top_case_country,
            top_case_cnt,
            most_age_group,
            least_age_group,
        ) = analyze_covid_impact(self.db)
        self.assertEqual(top_death_country, "Hungary")
        self.assertAlmostEqual(top_death_cnt, 1221, places=2)
        self.assertEqual(top_case_country, "Estonia")
        self.assertAlmostEqual(top_case_cnt, 35878, places=2)
        self.assertEqual(most_age_group, "15-24yr")
        self.assertEqual(least_age_group, "80+yr")


if __name__ == "__main__":
    unittest.main()
