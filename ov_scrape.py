######################################
## THIS CODE WORKS AS OF 2023-03-21 ##
######################################

#####################
## IMPORT PACKAGES ##
#####################

from ov_functions.ov_scraper import directory_manager, get_page_source
from ov_functions.ov_scraper import get_speech_links, date_of_speech
from ov_functions.ov_scraper import source_of_speech, title_of_speech
from ov_functions.ov_scraper import text_of_speech
from bs4 import BeautifulSoup
import requests

import re
import numpy as np
import pandas as pd

#######################
## DO SOME DIR SETUP ##
#######################

directory_manager()

####################
## SELENIUM SETUP ##
####################

main_url = 'https://miniszterelnok.hu/beszedek/'
page_source = get_page_source(main_url)

################################
## FIND LINKS TO ALL SPEECHES ##
##    USING BEAUTIFUL SOUP    ##
################################

title_urls = get_speech_links(page_source)

#################################
## GETTING ALL THE SPEECH DATA ##
#################################

speech_dates = []
speech_sources = []
speech_titles = []
speech_texts = []

for url in title_urls:

    # Scrape all pages with beautiful soup
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    date_regex = re.compile(r'\d{4}\.\d{2}\.\d{2}')
    source_regex = re.compile(r'Forrás:*')

    date_of_speech(soup, date_regex, speech_dates)
    source_of_speech(soup, source_regex, speech_sources)
    speech_title = title_of_speech(soup, speech_titles)
    text_of_speech(soup, source_regex, speech_title, speech_texts)

#################################
## CREATING THE BASE DATAFRAME ##
#################################

df = pd.DataFrame({'date': speech_dates,
                'source': speech_sources,
                'title': speech_titles,
                'text': speech_texts})

# Save the dataframe to a pickle file
df.to_pickle('dataframes/speeches_raw_df.pkl')
