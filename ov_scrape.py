######################################
## THIS CODE WORKS AS OF 2023-03-21 ##
######################################

######################
## IMPORT LIBRARIES ##
######################

import requests                     # This is used to make HTTP requests
from selenium import webdriver      # This performs actions in the browser
from bs4 import BeautifulSoup       # This is used to parse the HTML

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import os

import numpy as np
import pandas as pd

#######################
## DO SOME DIR SETUP ##
#######################

def directory_manager():
    # check if the 'data' subdirectory exists
    if not os.path.isdir('dataframes'):
        # create the 'data' subdirectory if it does not exist
        os.mkdir('dataframes')

directory_manager()

####################
## SELENIUM SETUP ##
####################

def get_page_source(url = 'https://miniszterelnok.hu/beszedek/'):

    # Set up the headless Chrome options
    chrome_options = Options()                          # Create the options instance
    chrome_options.add_argument('--headless')           # No visible browser window
    chrome_options.add_argument('--disable-gpu')        # Disable the GPU to speed things up

    # Set up the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Load the main Speeches page
    driver.get(url)

    # Click the "Load more" button until there are no more speeches to load
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="interjuk"]/div/div[3]/a')))
            show_more_button.click()
        except:
            break

    # Get the page source of the current page
    page_source = driver.page_source

    return page_source

page_source = get_page_source()

################################
## FIND LINKS TO ALL SPEECHES ##
##    USING BEAUTIFUL SOUP    ##
################################

def get_speech_links(page_source = page_source):
    # Create a BeautifulSoup object from the page source
    soup_main = BeautifulSoup(page_source, 'html.parser')

    # Find all the title links on the main page and extract their URLs
    title_links = soup_main.select('h3 a')
    title_urls = list(set([link['href'] for link in title_links]))  # For some reason there are duplicates

    return title_urls

title_urls = get_speech_links()

#################################
## GETTING ALL THE SPEECH DATA ##
#################################

def get_speech_data(urls = title_urls):
    speech_dates = []
    speech_sources = []
    speech_titles = []
    speech_texts = []

    for url in urls:
        # Scrape the first URL with beautiful soup
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        # Find the date of the speech
        date_regex = re.compile(r'\d{4}\.\d{2}\.\d{2}')
        speech_date = soup.find(text=date_regex).strip().replace('.', '-')
        speech_dates.append(speech_date)

        # Find source of the speech
        forras_regex = re.compile(r'Forrás:*')
        speech_source = soup.find(text=forras_regex).strip().replace('Forrás: ', '')
        speech_sources.append(speech_source)

        # Find the title of the speech
        speech_title = soup.find('h1').text
        speech_titles.append(speech_title)

        # Find the text of the speech
        speech_text = ''
        # Loop through all p elements
        for p in soup.find_all('p'):
            # If the p element has a class attribute, skip it
            if p.has_attr('class'):
                continue
            # Otherwise, add the text to the speech_text variable
            else:
                speech_text += p.text + ' '

        remove_beginning = 'Beszédek / '
        remove_end = 'orbanviktor@orbanviktor.huOrbán Viktor1357 Budapest, Pf. 1'

        speech_text = speech_text.replace(remove_beginning, '')
        speech_text = speech_text.replace(speech_title, '')
        speech_text = speech_text.replace(remove_end, '')
        speech_text = speech_text.strip()

        speech_texts.append(speech_text)

    #################################
    ## CREATING THE BASE DATAFRAME ##
    #################################

    # Create a dataframe from the lists
    df = pd.DataFrame({'date': speech_dates,
                    'source': speech_sources,
                    'title': speech_titles,
                    'text': speech_texts})

    return df

df = get_speech_data()

# Save the dataframe to a pickle file
df.to_pickle('dataframes/speeches.pkl')