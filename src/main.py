# Imports
from language_loader import LanguageLoader
from language_changing_process import LanguageChangingProcess
from user_getter import *
from project_getter import *
from studio_getter import *
from file_viewer import *
from rich import print as rprint
import questionary
import requests
import os

# Constants
API = "https://api.scratch.mit.edu"

# Initial setting up
clear()
os.system("title Scratchgetter")

# This exception will end the program
class End(Exception):
    pass

# Main loop
class App:
    def __init__(self):
        # Version number and stage
        self.version = "1.0.0"
        self.stage = None

        # Getting language
        self.get_language()

        # Processes
        self.initial_internet_check()
        self.main()

    def get_language(self):
        self.ll = LanguageLoader()  # ll - language loader
        self.ld = self.ll.data  # ld - language data

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
                print(self.ld["introduction"]["restartInfo"])
                print(self.ld["introduction"]["legalNotice"])
                break_line()

                user_input = questionary.select(
                    self.ld["introduction"]["optionsQuery"],
                    choices=self.ld["introduction"]["options"]
                ).unsafe_ask()
                break_line()

                if user_input == self.ld["introduction"]["options"][0]:
                    self.user_process = UserProcess(self)

                elif user_input == self.ld["introduction"]["options"][1]:
                    self.project_process = ProjectProcess(self)

                elif user_input == self.ld["introduction"]["options"][2]:
                    self.studio_process = StudioProcess(self)

                elif user_input == user_input == self.ld["introduction"]["options"][3]:
                    self.file_viewer = FileViewer(self)

                elif user_input == self.ld["introduction"]["options"][4]:
                    self.language_changing_process = LanguageChangingProcess(self)

                else:
                    clear()
                    raise End

        except ConnectionError:
            clear()
            rprint("[red]" + self.ld["tests"]["internetConnectionFailure"])
            await_enter(self.ld, to_exit=True)
            clear()
            raise End


# Eternal program that ends only when the user picks the quit option
while True:
    try:
        app = App()

    except KeyboardInterrupt:
        clear()
        print(LanguageLoader().data["reusable"]["restartDetected"]) # reloads language
        continue

    except End:
        break

clear()
