from bs4 import BeautifulSoup
import pandas as pd
import requests

class Scraper():
    def __init__(self, state_abbrev, city_or_town):
        self.state_abbrev = state_abbrev
        self.city_or_town = city_or_town

        self.real_estate_link = f'https://www.neighborhoodscout.com/{state_abbrev}/{city_or_town}/real-estate'
        self.crime_link = f'https://www.neighborhoodscout.com/{state_abbrev}/{city_or_town}/crime'

    def Report_Data(self, report_type):
        try:
            if report_type == 'real_estate':
                data = self.get_real_estate()
                data = self.cast_datatypes(data)
                return data
            if report_type == 'crime':
                data = self.get_crime()
                data = self.cast_datatypes(data)
                return data
        except: # the app will automatically try to run the scraper with None inputs when switching tabs
            return None

    def get_real_estate(self):
        r = requests.get(self.real_estate_link + '#data')
        soup = BeautifulSoup(r.text, 'html.parser')

        percentages = soup.find_all('div', class_='horizontal-bar-chart-label horizontal-bar-chart-label-outer')
        percentage_bin = []
        for percent in percentages:
            percentage_bin.append(percent.text.replace('\n', ''))

        general_stats = soup.find_all('span', class_='em')
        stats_bin = []
        for stat in general_stats:
            stats_bin.append(stat.text)

        # General stats
        median_home_value = stats_bin[0]
        num_homes_and_apts = stats_bin[1]
        avg_mkt_rent = stats_bin[2]

        # Homeownership rate
        owners = percentage_bin[9]
        renters = percentage_bin[10]
        vacant = percentage_bin[11]

        # Age of homes
        newer = percentage_bin[12] # 2000 or newer
        new = percentage_bin[13] # 1970-1999
        old = percentage_bin[14] # 1940-1969
        older = percentage_bin[15] # 1939 or older

        # Types of homes
        single_family_homes = percentage_bin[16]
        townhomes = percentage_bin[17]
        small_apt_buildings = percentage_bin[18]
        apt_complexes = percentage_bin[19]
        mobile_homes = percentage_bin[20]
        other_home_types = percentage_bin[21]

        # Bedroom count
        no_bedroom = percentage_bin[22]
        one_bedroom = percentage_bin[23]
        two_bedrooms = percentage_bin[24]
        three_bedrooms = percentage_bin[25]
        four_bedrooms = percentage_bin[26]
        five_or_more_bedrooms = percentage_bin[27]

        data = {
            'median_home_value': median_home_value,
            'num_homes_and_apts': num_homes_and_apts,
            'avg_mkt_rent': avg_mkt_rent,
            'owners': owners,
            'renters': renters,
            'vacant': vacant,
            'newer': newer,
            'new': new,
            'old': old,
            'older': older,
            'single_family_homes': single_family_homes,
            'townhomes': townhomes,
            'small_apt_buildings': small_apt_buildings,
            'apt_complexes': apt_complexes,
            'mobile_homes': mobile_homes,
            'other_home_types': other_home_types,
            'no_bedroom': no_bedroom,
            'one_bedroom': one_bedroom,
            'two_bedrooms': two_bedrooms,
            'three_bedrooms': three_bedrooms,
            'four_bedrooms': four_bedrooms,
            'five_or_more_bedrooms': five_or_more_bedrooms
        }
        return data

    def get_crime(self):
        r = requests.get(self.crime_link + '#data')
        soup = BeautifulSoup(r.text, 'html.parser')

        strongs = soup.find_all('strong')
        strongs_bin = []
        for strong in strongs:
            strongs_bin.append(strong.text)

        # Crime index
        crime_index = soup.find('h1', class_='score').text

        # Annual crimes
        num_violent_crimes = strongs_bin[4]
        num_property_crimes = strongs_bin[5]
        num_total_crimes = strongs_bin[6]

        # Crime rate per 1000 residents
        violent_crimes_per_1000 = strongs_bin[7]
        property_crimes_per_1000 = strongs_bin[8]
        total_crimes_per_1000 = strongs_bin[9]

        data = {
            'crime_index': crime_index,
            'num_violent_crimes': num_violent_crimes,
            'num_property_crimes': num_property_crimes,
            'num_total_crimes': num_total_crimes,
            'violent_crimes_per_1000': violent_crimes_per_1000,
            'property_crimes_per_1000': property_crimes_per_1000,
            'total_crimes_per_1000': total_crimes_per_1000
        }
        return data

    def cast_datatypes(self, data):
        mappings = data.keys()
        data = data.values()

        data = [d.replace('$', '') for d in data]
        data = [d.replace(',', '') for d in data]
        data = [d.replace('%', '') for d in data]
        data = [float(d) for d in data]

        data = pd.Series(data, index=mappings)
        return data
