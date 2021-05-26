# Scraper for the office scripts
import requests
from bs4 import BeautifulSoup

from WebObject import WebObject

BASE_URL = 'https://transcripts.foreverdreaming.org/viewforum.php?f=574'
BASE_BASE_URL = 'https://transcripts.foreverdreaming.org/'
PAGES = '&start='
PAGINATION_QUANTITY = 25
CURRENT_PAGE = 0
MAX_PAGINATION = 175
PAGE = ""
allatags = []

officeObjects = []

def parseHtml(page):
    soup = BeautifulSoup(page.content, 'html.parser')

    allatags.extend(collect_all_a_tags(soup))

    #for title in allatags:
        #link = title.find('a')['href']

        #print(title.text , title['href'], end='\n')

def collect_all_a_tags(soupResult):
    return soupResult.find_all('a', class_='topictitle')


def generate_page():
    if CURRENT_PAGE == 0:
        return BASE_URL
    else:
        newUrl = BASE_URL + PAGES
        return newUrl + str(CURRENT_PAGE)

def convertToObject(unstructured):
    for records in unstructured:
        officeObjects.append(WebObject(records.text, records['href']))

def downloadScriptFor(episode):
    episode = BASE_BASE_URL + episode.urlAddress[2:]
    downloadFile = requests.get(episode)
    soup = BeautifulSoup(downloadFile.content, 'html.parser')
    dialog = soup.find_all('p')
    #for test in dialog:
        #print(test)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while CURRENT_PAGE <= MAX_PAGINATION:
        url = generate_page()

        PAGE = requests.get(url)
        parseHtml(PAGE)
        CURRENT_PAGE += PAGINATION_QUANTITY

    #Converts all the unstructured html tags to objects
    convertToObject(allatags)

    downloadScriptFor(officeObjects[1])

    print(len(officeObjects))