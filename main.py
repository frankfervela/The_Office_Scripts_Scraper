# Scraper for the office scripts
import requests
from bs4 import BeautifulSoup
import os
from WebObject import WebObject

#region GLOBAL VARIABLES
BASE_URL = 'https://transcripts.foreverdreaming.org/viewforum.php?f=574'
BASE_BASE_URL = 'https://transcripts.foreverdreaming.org/'
PAGES = '&start='
PAGINATION_QUANTITY = 25
CURRENT_PAGE = 0
MAX_PAGINATION = 175
PAGE = ""
ALL_A_TAGS_FROM_EPISODE_LIST = []

OFFICE_OBJECTS = []

# Directory
DIRECTORY = "The Office Scripts"

# Parent Directory path
PARENT_DIR = "./"

# Path
DIRECTORY_PATH = os.path.join(PARENT_DIR, DIRECTORY)

#endregion

#region METHODS

#Getting the tags from the entire list of episodes and storing them in a global array
def parseHtml(page):
    soup = BeautifulSoup(page.content, 'html.parser')

    ALL_A_TAGS_FROM_EPISODE_LIST.extend(collect_all_a_tags(soup))

# Collect al tags that have the episode link and name
def collect_all_a_tags(soupResult):
    return soupResult.find_all('a', class_='topictitle')


#Generating a url depending on the page the loop is on. The difference in each url is
# the pagination number that happens to be 25 more than the previous page, starting at 0
def generate_url():
    if CURRENT_PAGE == 0:
        return BASE_URL
    else:
        newUrl = BASE_URL + PAGES
        return newUrl + str(CURRENT_PAGE)

#Processing the raw tags into managable objects
def convertToObject(unstructured):
    for records in unstructured:
        OFFICE_OBJECTS.append(WebObject(records.text, records['href']))

#Downloading the tags containing the script information
def downloadScriptFor(episode):

    print(f'Generating script file for {episode.fileName}', '\n')
    episode = BASE_BASE_URL + episode.urlAddress[2:]
    downloadFile = requests.get(episode)
    soup = BeautifulSoup(downloadFile.content, 'html.parser')
    dialog = soup.find_all('p')


    return dialog

#Generating all script files
def GenerateScriptFiles():

    for episode in OFFICE_OBJECTS:
        if episode.fileName == 'Please Read Updates: Take the 2021 Challenge!':
            continue

        downloadedDialog = downloadScriptFor(episode)

        cleanName = episode.fileName.replace('/', "")
        cleanName = cleanName.replace('?', "")
        cleanName = cleanName.replace('*', "")

        with open(f"{DIRECTORY_PATH}/{cleanName}.txt", "x", encoding="utf-8") as filehandle:
            for line in downloadedDialog:
                filehandle.write(f'{line.text}\n')


def GenerateDirectory():
    # Creating the directory to store the script files once downloaded
    try:
        if os.path.exists(DIRECTORY_PATH):
            os.rmdir(DIRECTORY_PATH)

        os.mkdir(DIRECTORY_PATH)
        print("Directory '% s' created" % DIRECTORY)

    except OSError as error:
        print(error)

#endregion

#MAIN
if __name__ == '__main__':

    GenerateDirectory()

    try:
        while CURRENT_PAGE <= MAX_PAGINATION:
            url = generate_url()

            PAGE = requests.get(url)
            parseHtml(PAGE)
            CURRENT_PAGE += PAGINATION_QUANTITY

        # Converts all the unstructured html tags to objects
        convertToObject(ALL_A_TAGS_FROM_EPISODE_LIST)

        GenerateScriptFiles()

        print('Scripts downloaded')

    except OSError as error:
        print(error)


