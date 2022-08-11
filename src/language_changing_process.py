# Imports
from tools import *
import os
import toml
import questionary

# LanguageChangingProcess class
class LanguageChangingProcess:
    def __init__(self, master):
        # Inheriting
        self.master = master
        self.ll = self.master.ll
        self.ld = self.master.ld

        # Beginning process
        self.begin_process()

    def reveal_valid_languages(self, valid_languages):
        for i in range(len(valid_languages)):
            language = valid_languages[i]
            print(f"{i + 1 }. {language['meta']['name']}")
            print(f"{self.ld['language_changing']['author']} {language['meta']['author']}")
            print(f"{self.ld['language_changing']['description']} {language['meta']['description']}")
            break_line()

    def get_valid_languages(self):
        valid_languages = []
        for file in [x for x in os.listdir(os.getcwd() + "\\languages\\") if x.split(".")[1] == "toml"]:
            try:
                language = toml.load(os.getcwd() + "\\languages\\" + file)
                if os.path.exists(os.getcwd() + "\\date_formatters\\" + language["linked"]["dateFormatterFile"].split(".")[-1] + ".py") and language["meta"]["for_version"] == self.master.version:
                    valid_languages.append(language)
            except toml.TomlDecodeError: # if language doesn't have valid info
                continue
            except KeyError: # if language misses necessary information
                continue

        return valid_languages

    def find_language_filename_by_name(self, languages, language):
        for element in languages:
            if element["meta"]["name"] == language:
                return element["meta"]["file_name"]

    def get_user_input(self, valid_languages):
        options = [x["meta"]["name"] for x in valid_languages]
        options.remove(self.ld["meta"]["name"])
        options.append(self.ld["reusable"]["cancel"])

        return questionary.select(
            self.ld["language_changing"]["selectLanguageQuery"],
            choices=options
        ).unsafe_ask()

    def begin_process(self):
        clear()
        print(self.ld["language_changing"]["introduction"])

        self.valid_languages = self.get_valid_languages()
        if len(self.valid_languages) >= 2:
            self.reveal_valid_languages(self.valid_languages)

            self.user_input = self.get_user_input(self.valid_languages)
            if self.user_input != self.ld["reusable"]["cancel"]:
                new_data = toml.load(os.getcwd() + "\\conf.toml") # so that other data doesn't go ignored
                new_data["language"] = self.find_language_filename_by_name(self.valid_languages, self.user_input)
                toml.dump(new_data, open(os.getcwd() + "\\conf.toml", "w"))
                print(self.ld["language_changing"]["restartNeeded"])
                await_enter(self.ld, to_exit=True)
        elif len(self.valid_languages) == 1:
            clear()
            print(self.ld["language_changing"]["ifOne"])
            await_enter(self.ld)
        else:  # if 0
            clear()
            print(self.ld["language_changing"]["ifZero"])
            await_enter(self.ld, to_exit=True)
            quit()
        clear()

