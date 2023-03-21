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

class DirectoryManager:
    @staticmethod
    def create_directory():
        if not os.path.isdir('dataframes'):
            os.mkdir('dataframes')

class PageSource:
    @staticmethod
    def get_page_source(url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        while True:
            try:
                show_more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="interjuk"]/div/div[3]/a')))
                show_more_button.click()
            except:
                break
        page_source = driver.page_source
        return page_source

class SpeechLinks:
    @staticmethod
    def get_speech_links(page_source):
        soup_main = BeautifulSoup(page_source, 'html.parser')
        title_links = soup_main.select('h3 a')
        title_urls = list(set([link['href'] for link in title_links]))
        return title_urls

class SpeechInfo:
    def __init__(self, soup):
        self.soup = soup
        self.speech_titles = []
        self.speech_dates = []
        self.speech_sources = []
        self.speech_texts = []

    def get_speech_info(self):
        self.title_of_speech()
        self.date_of_speech()
        self.source_of_speech()
        self.text_of_speech()

    def date_of_speech(self, date_regex='Időpont:'):
        speech_date = self.soup.find(string=date_regex).strip().replace('.', '-')
        self.speech_dates.append(speech_date)

    def source_of_speech(self, source_regex='Forrás: '):
        speech_source = self.soup.find(string=source_regex).strip().replace('Forrás: ', '')
        self.speech_sources.append(speech_source)

    def title_of_speech(self):
        speech_title = self.soup.find('h1').text
        self.speech_titles.append(speech_title)
        return speech_title

    def text_of_speech(self, source_regex='forrás:'):
        speech_text = ''
        for p in self.soup.find_all('p'):
            if p.has_attr('class'):
                continue
            else:
                speech_text += p.text + ' '

        remove_beginning = 'Beszédek / '
        remove_email = 'orbanviktor@orbanviktor.hu'
        remove_address = 'Orbán Viktor1357 Budapest, Pf. 1'
        speech_text = speech_text.replace(remove_beginning, '')
        speech_text = speech_text.replace(self.speech_titles[0], '')
        speech_text = speech_text.replace(remove_email, '')
        speech_text = speech_text.replace(remove_address, '')
        speech_text = speech_text.strip()

        if speech_text == '':
            speech_text = self.soup.find(string=source_regex).find_next('div', class_='elementor-widget-container')
            speech_text = speech_text.text.strip()

        self.speech_texts.append(speech_text)
