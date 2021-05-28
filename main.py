# Scraper for the office scripts
# Thanks for https://transcripts.foreverdreaming.org for
import requests
from bs4 import BeautifulSoup
import os
from WebObject import WebObject

# region GLOBAL VARIABLES
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
# endregion

# region METHODS

# Getting the tags from the entire list of episodes and storing them in a global array
def parse_html(page):
    soup = BeautifulSoup(page.content, 'html.parser')

    ALL_A_TAGS_FROM_EPISODE_LIST.extend(collect_all_a_tags(soup))


# Collect al tags that have the episode link and name
def collect_all_a_tags(soup_result):
    return soup_result.find_all('a', class_='topictitle')


# Generating a url depending on the page the loop is on. The difference in each url is
# the pagination number that happens to be 25 more than the previous page, starting at 0
def generate_url():
    if CURRENT_PAGE == 0:
        return BASE_URL
    else:
        new_url = BASE_URL + PAGES
        return new_url + str(CURRENT_PAGE)


# Processing the raw tags into manageable objects
def convert_to_object(unstructured):
    for records in unstructured:
        OFFICE_OBJECTS.append(WebObject(records.text, records['href']))


# Downloading the tags containing the script information
def download_script_for(episode):
    print(f'Generating script file for {episode.fileName}', '\n')
    episode = BASE_BASE_URL + episode.urlAddress[2:]
    download_file = requests.get(episode)
    soup = BeautifulSoup(download_file.content, 'html.parser')
    dialog = soup.find_all('p')

    return dialog


# Generating all script files
def generate_script_files():
    for episode in OFFICE_OBJECTS:
        if episode.fileName == 'Please Read Updates: Take the 2021 Challenge!':
            continue

        downloaded_dialog = download_script_for(episode)

        clean_name = episode.fileName.replace('/', "")
        clean_name = clean_name.replace('?', "")
        clean_name = clean_name.replace('*', "")

        with open(f"{DIRECTORY_PATH}/{clean_name}.txt", "x", encoding="utf-8") as file_handler:
            for line in downloaded_dialog:
                file_handler.write(f'{line.text}\n')


def generate_directory():
    # Creating the directory to store the script files once downloaded
    try:
        if os.path.exists(DIRECTORY_PATH):
            os.rmdir(DIRECTORY_PATH)

        os.mkdir(DIRECTORY_PATH)
        print("Directory '% s' created" % DIRECTORY)

    except OSError as err:
        print(err)


# endregion

# MAIN
if __name__ == '__main__':

    generate_directory()

    try:
        while CURRENT_PAGE <= MAX_PAGINATION:
            url = generate_url()

            PAGE = requests.get(url)
            parse_html(PAGE)
            CURRENT_PAGE += PAGINATION_QUANTITY

        # Converts all the unstructured html tags to objects
        convert_to_object(ALL_A_TAGS_FROM_EPISODE_LIST)

        generate_script_files()

        print('Scripts downloaded')

    except OSError as error:
        print(error)
