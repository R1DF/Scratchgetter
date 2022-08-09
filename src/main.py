# Imports
from language_loader import LanguageLoader
from language_changing_process import LanguageChangingProcess
from user_getter import *
from project_getter import *
from studio_getter import *
import questionary
import requests
import os

# Constants
API = "https://api.scratch.mit.edu"

# Initial setting up
clear()
os.system("title Scratchgetter")

# Main loop
class App:
    def __init__(self):
        # Version number
        self.version = "1.0.0"

        # Getting language
        self.ll = LanguageLoader()  # ll - language loader
        self.ld = self.ll.data  # ld - language data

        # Processes
        self.initial_internet_check()
        self.main()

    def initial_internet_check(self):
        print(self.ld["tests"]["testingConnection"])
        try:
            test_request = requests.get(API)
            print(self.ld["tests"]["requestData"], test_request)
            print(self.ld["tests"]["internetConnectionSuccess"])
            break_line()
            await_enter(self.ld)
            clear()

        except requests.ConnectionError:
            print(self.ld["tests"]["internetConnectionFailure"])
            await_enter(self.ld, to_exit=True)
            clear()
            quit()

    def main(self):
        try:
            while True:
                print(self.ld["introduction"]["welcome"])
                print(self.ld["introduction"]["legalNotice"])
                break_line()

                user_input = questionary.select(
                    self.ld["introduction"]["optionsQuery"],
                    choices=self.ld["introduction"]["options"]
                ).ask()
                break_line()

                if user_input == self.ld["introduction"]["options"][0]:
                    self.user_process = UserProcess(self)

                elif user_input == self.ld["introduction"]["options"][1]:
                    self.project_process = ProjectProcess(self)
                elif user_input == self.ld["introduction"]["options"][2]:
                    self.studio_process = StudioProcess(self)
                elif user_input == self.ld["introduction"]["options"][3]:
                    self.language_changing_process = LanguageChangingProcess(self)
                else:
                    clear()
                    quit()

        except ConnectionError:
            clear()
            print(self.ld["tests"]["internetConnectionFailure"])
            await_enter(self.ld, to_exit=True)
            clear()
            quit()


# Creating App instance
app = App()
