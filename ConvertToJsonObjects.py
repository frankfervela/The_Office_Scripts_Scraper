import os


def convert_files_to_json():

    list_of_json = []

    listOfDirs = sorted(os.listdir("The Office Scripts"))

    for filename in listOfDirs:
        with open('The Office Scripts/' + filename, 'r') as file:
            text = file.readlines()
            print(text[1])


convert_files_to_json()