# Load libraries
import sys
sys.path.insert(0, '.gitignore')

import config
import requests
import pandas as pd

# Define function for geocoder
def get_lat_long(query):
    # Set config
    lat, lng = None, None
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
    except:
        pass
    return lat, lng

# Import names to query geocoder
pass_info = pd.read_csv('web-scraping/data/pass_info.csv')
resorts_dict = pass_info[['short-name','resort']].set_index('short-name').to_dict()['resort']

# Geocode Resorts
resort_locations = {}

for name, query in resorts_dict.items():
    lat, lng = get_lat_long(query)
    resort_locations[name] = {'lat':lat, 'lng':lng}

# Export locations
resort_locations = pd.DataFrame.from_dict(resort_locations, orient='index')
resort_locations = resort_locations.reset_index()
resort_locations = resort_locations.rename(columns={'index':'short-name'})
resort_locations.to_csv('web-scraping/data/raw_resort_locations.csv', index = False)