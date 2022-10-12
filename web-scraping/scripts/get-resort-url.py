# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# Configure selenium options
options = Options()
options.headless = False
options.add_argument("--window-size=500,1200")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define urls for resort lists for each pass
url = {'mountain-collective':'https://www.onthesnow.com/mountain-collective/ski-resorts',
       'epic-pass': 'https://www.onthesnow.com/epic-pass/ski-resorts',
       'ikon-pass': 'https://www.onthesnow.com/ikon-pass/ski-resorts'}

# Initialise empty dict to store pass info
pass_info = {'pass':[], 
             'resort':[], 
             'link':[]} 

# Function to check if element exists
def check_exists_by_css(css_selector):
    try:
        driver.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException:
        return False
    return True

# Check if view all resorts button exists - if so, click it
def click_view_all_resorts(button):
    buttons = driver.find_elements(By.CSS_SELECTOR, button)
    for button in buttons:
        try:
            button.click()
        except ElementNotInteractableException:
            print('Element not interactable')
        print('Clicked')

# Function to scrape list of resorts included in each pass
def get_resort_list(name, url):
    driver.get(url)

    button = 'button.styles_btnViewAllResorts__12uob'
    if check_exists_by_css(button):
        click_view_all_resorts(button)
    
    # Select resortList element
    resorts = driver.find_element(By.CLASS_NAME, "md-show.m-0")
    resort_list = resorts.find_elements(By.TAG_NAME, 'a')
    
    for resort in resort_list:
        resort_pass = name
        resort_name = resort.get_attribute("innerHTML")
        resort_link = resort.get_attribute("href")

        pass_info['pass'].append(name)
        pass_info['resort'].append(resort_name)
        pass_info['link'].append(resort_link)


# Scrape list of resorts for each pass
# get_resort_list('epic-pass', url['epic-pass'])
for pass_name, pass_url in url.items():
    get_resort_list(pass_name, pass_url)

df_pass_info = pd.DataFrame.from_dict(pass_info)

# Get short-name from url
df_pass_info['short-name'] = df_pass_info['link'].str.split('/').str[4]

# Write to csv
df_pass_info.to_csv('web-scraping/data/pass_info.csv', index=False)

# Close browser
driver.quit()