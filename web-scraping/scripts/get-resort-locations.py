# Load libraries
import sys
sys.path.insert(0, '.gitignore')

import config
import requests
import pandas as pd

# Define function for getting country from google geocode response
def get_country(response):
    results = response.json()['results']
    address_components = results[0]['address_components']

    for i in range(0,len(address_components)):
        if address_components[i]['types'][0] == 'country':
            return address_components[i]['short_name'], address_components[i]['long_name']
    return None
        
# Define function for geocoder
def geocode(query):
    # Set config
    lat, lng, country_short, country_long = None, None, None, None
    api_key = config.API_KEY
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    endpoint = f'{base_url}?address={query}&key={api_key}'

    # Make api call
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']

        country_short, country_long = get_country(r)
    except:
        pass
    return lat, lng, country_short, country_long

# Import names to query geocoder
pass_info = pd.read_csv('web-scraping/data/pass_info.csv')
resorts_dict = pass_info[['short-name','resort']].set_index('short-name').to_dict()['resort']

# Geocode Resorts
resort_locations = {}

for name, query in resorts_dict.items():
    lat, lng, country_short, country_long = geocode(query)
    resort_locations[name] = {'lat':lat, 'lng':lng, 'country-short':country_short, 'country-long':country_long}

# Convert to df
resort_locations = pd.DataFrame.from_dict(resort_locations, orient='index')
resort_locations = resort_locations.reset_index()
resort_locations = resort_locations.rename(columns={'index':'short-name'})

# Mitigation for missing values
resort_locations.loc[resort_locations['short-name'] == 'boyne-highlands',['lat','lng', 'country-short', 'country-long']] = [45.464836748744645, -84.92655645968269, 'US', 'United States']
resort_locations.loc[resort_locations['short-name'] == 'keystone',['lat','lng', 'country-short', 'country-long']] = [39.607802758569356, -105.94376561689656, 'US', 'United States']
resort_locations.loc[resort_locations['short-name'] == 'big-sky-resort',['lat','lng', 'country-short', 'country-long']] = [45.2859326883829, -111.40120760189154, 'US', 'United States']

# Export locations
resort_locations.to_csv('web-scraping/data/raw_resort_locations.csv', index = False)