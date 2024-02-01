import time
import sqlite3
import json

from selenium import webdriver
from bs4 import BeautifulSoup

from .models import Outlet

def scrape_and_save_to_db(url, num_locations):
    # using selenium to load the page and execute javascript, because the items are generated using javascript
    # ChromeDriver needed here
    driver = webdriver.Chrome()  
    driver.get(url)

    # sleep time can be adjusted (waiting for js to load)
    time.sleep(5)

    page_source = driver.page_source
    driver.quit()

    # using bs to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # look for main container holding all the items
    nested_div = soup.find('div', {'class': 't3-wrapper'}).find('div', {'class': 't3-mainbody'}).find('div', {'class': 'row'}).find('div', {'class': 't3-content col-xs-12'}).find('div', {'class': 'fp-map-view legend_left store_locator'}).find('div', {'class': 'clearfix'}).find('div', {'class': 'tab-container'}).find('div', {'class': 'tab-content'}).find('div', {'class': 'tab-pane active'}).find('div', {'class': 'fp_side fp_left'}).find('div', {'id': 'fp_googleMapSidebar'}).find('div', {'id': 'fp_locationlist'}).find('div', {'class': 'fp_ll_holder'})

    if nested_div:
        for i in range(1, num_locations + 1):
            location_item = nested_div.find('div', class_=f'fp_listitem fp_list_marker{i}')

            if location_item:
                print(f"Found location {i}")

                # initialise variables
                outlet = ''
                address = ''
                opening_hours = []
                waze_link = ''
                google_link = ''
                latitude = 0.0
                longitude = 0.0

                latitude = float(location_item.get('data-latitude', 0.0))
                longitude = float(location_item.get('data-longitude', 0.0))

                # look for location_left and location_right divs
                # one holds info the other holds links
                location_left = location_item.find('div', class_='location_left')
                location_right = location_item.find('div', class_='location_right')

                if location_left:
                    outlet = location_left.find('h4').get_text(strip=True)

                    # look into infoboxcontent and extract all p elements excluding the one with class 'infoboxlink'
                    # 'infoboxlink' contains no useful information only 'find out more' message
                    infoboxcontent = location_left.find('div', class_='infoboxcontent')
                    if infoboxcontent:
                        paragraphs = [paragraph.get_text(strip=True) for paragraph in infoboxcontent.find_all('p', class_=lambda x: x != 'infoboxlink')]

                        # first paragraph is always the address
                        if paragraphs:
                            address = paragraphs[0]

                            # extract the rest of the paragraphs as opening hours
                            opening_hours = paragraphs[1:]

                if location_right:
                    direction_button_div = location_right.find('div', class_='directionButton')

                    if direction_button_div:
                        # extract links from 'a' elements in direction_button_div
                        links = direction_button_div.find_all('a', href=True)

                        # assume there are always two links & the links point to waze and google respectively
                        if len(links) >= 2:
                            waze_link = links[0]['href']
                            google_link = links[1]['href']

                # insert data into db
                outlet = Outlet(
                    name=outlet,
                    address=address,
                    opening_hours=json.dumps(opening_hours),
                    waze_link=waze_link,
                    google_link=google_link,
                    latitude=latitude,
                    longitude=longitude
                )
                outlet.save()
    print("Scraping and database insertion successful.")