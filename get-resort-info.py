# Load libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# Configure selenium options
options = Options()
options.headless = False
options.add_argument("--window-size=500,1200")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load pass info csv
pass_info = pd.read_csv('web-scraping/data/pass_info.csv')

# Create dict for scraping individual resort pages
resorts_dict = pass_info[['short-name','link']].set_index('short-name').to_dict()['link']

# Average snowfall
def get_snowfall_overview():
    average_snowfall = driver.find_element(By.CLASS_NAME, 'styles_data__2doiC')

    snowfall_month = []
    snowfall_amount = []

    months = average_snowfall.find_elements(By.CLASS_NAME, 'styles_date__ACGKW')
    amounts = average_snowfall.find_elements(By.CLASS_NAME, 'styles_value__3uWEv')

    for month in months:
            snowfall_month.append(month.get_attribute('innerHTML'))
    for amount in amounts:
            snowfall_amount.append(amount.get_attribute('innerHTML'))

    snowfall_info = dict(zip(snowfall_month, snowfall_amount))
    return snowfall_info


# Terrain overview
def get_terrain_overview():
    terrain_overview = driver.find_elements(By.CLASS_NAME, 'styles_box__1xP75')

    terrain_statistics = []
    terrain_values = []

    for item in terrain_overview:
        statistics = item.find_elements(By.CLASS_NAME, 'styles_secondary__2Uu9u')
        values = item.find_elements(By.CLASS_NAME, 'styles_value__fB0LV')

        for statistic in statistics:
            terrain_statistics.append(statistic.get_attribute('innerHTML'))
        for value in values:
            terrain_values.append(value.get_attribute('innerHTML'))

    terrain_info = dict(zip(terrain_statistics, terrain_values))
    return terrain_info

# Lift overview
def get_lift_overview():
    lift_overview = driver.find_element(By.CLASS_NAME, 'styles_box__1sXJN.styles_box__1j4nK')

    lift_type = []
    lift_value = []

    lift_types = lift_overview.find_elements(By.CLASS_NAME, 'styles_secondary__2Uu9u')
    lift_count = lift_overview.find_elements(By.CLASS_NAME, 'styles_value__fB0LV')

    for lift in lift_types:
        lift_type.append(lift.get_attribute('innerHTML'))
    for count in lift_count:
        lift_value.append(count.get_attribute('innerHTML'))

    lift_info = dict(zip(lift_type, lift_value))
    return lift_info

# Get elevation overview
def get_elevation_overview():
    elevation_overview = driver.find_element(By.CLASS_NAME, 'styles_box__1sXJN.styles_box__3vF_V')

    elevation_statistic = []
    elevation_value = []

    statistics = elevation_overview.find_elements(By.CLASS_NAME, 'styles_name__3jgKM')
    values = elevation_overview.find_elements(By.CLASS_NAME, 'styles_distance__3eFw3')

    for statistic in statistics:
        elevation_statistic.append(statistic.get_attribute('innerHTML'))
    for value in values:
        elevation_value.append(value.get_attribute('innerHTML'))

    elevation_info = dict(zip(elevation_statistic, elevation_value))
    return elevation_info    


# # Get resort info
# for url in url_list:

#     # Connect driver
#     driver.get(url)

#     # Scrape data
#     get_lift_overview()
    get_snowfall_overview()
    get_terrain_overview()
    get_elevation_overview()


# Lifts Overview
resort_lifts = {}
resort_snowfall = {}
resort_terrain = {}
resort_elevation = {}

for name, url in resorts_dict.items():
    print('*-----------------------*')
    print(f'starting scrape for: {name}')
    driver.get(url)

    print('scraping lifts')
    lifts = get_lift_overview()

    print('scraping snowfall')
    snowfall = get_snowfall_overview()

    print('scraping terrain')
    terrain = get_terrain_overview()

    print('scraping elevation')
    elevation = get_elevation_overview()
    
    resort_lifts[name] = lifts
    resort_snowfall[name] = snowfall
    resort_terrain[name] = terrain
    resort_elevation[name] = elevation

# Export Lifts
resort_lifts = pd.DataFrame.from_dict(resort_lifts, orient='index')
resort_lifts = resort_lifts.reset_index()
resort_lifts = resort_lifts.rename(columns={'index':'short-name'})
resort_lifts.to_csv('web-scraping/data/raw_resort_lifts.csv', index = False)

# Export Snowfall
resort_snowfall = pd.DataFrame.from_dict(resort_snowfall, orient='index')
resort_snowfall = resort_snowfall.reset_index()
resort_snowfall = resort_snowfall.rename(columns={'index':'short-name'})
resort_snowfall.to_csv('web-scraping/data/raw_resort_snowfall.csv', index = False)

# Export Terrain
resort_terrain = pd.DataFrame.from_dict(resort_terrain, orient='index')
resort_terrain = resort_terrain.reset_index()
resort_terrain = resort_terrain.rename(columns={'index':'short-name'})
resort_terrain.to_csv('web-scraping/data/raw_resort_terrain.csv', index = False)

# Export Elevation
resort_elevation = pd.DataFrame.from_dict(resort_elevation, orient='index')
resort_elevation = resort_elevation.reset_index()
resort_elevation = resort_elevation.rename(columns={'index':'short-name'})
resort_elevation.to_csv('web-scraping/data/raw_resort_elevation.csv', index = False)

# Close browser
driver.quit()