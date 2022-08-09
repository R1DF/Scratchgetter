# Imports
from tools import *
import questionary
import os
import toml


# FileViewer class
class FileViewer:
    def __init__(self, master):
        # Inheriting
        self.master = master
        self.ll = self.master.ll
        self.ld = self.master.ld

        # Directory asking
        while True:
            clear()
            in_default_location = questionary.select(
                self.ld["view_file"]["inDefaultPathQuery"],
                choices=[
                    self.ld["reusable"]["yes"],
                    self.ld["reusable"]["no"],
                    self.ld["reusable"]["cancel"]
                ]
            ).ask()

            if in_default_location == self.ld["reusable"]["yes"]:
                file_type = questionary.select(
                    self.ld["view_file"]["selectPathQuery"],
                    choices=self.ld["view_file"]["options"]
                ).ask()

                path = os.getcwd() + "\\saves\\" + {
                    self.ld["view_file"]["options"][0]: "\\users\\",
                    self.ld["view_file"]["options"][1]: "\\projects\\",
                    self.ld["view_file"]["options"][2]: "\\studios\\"

                }[file_type]
            elif in_default_location == self.ld["reusable"]["no"]:
                path = questionary.path(
                    self.ld["view_file"]["enterPathQuery"],
                    default=os.getcwd(),
                    only_directories=True
                ).ask() + "\\"
            else:
                clear()
                return

            # Finding all toml files
            files = self.find_all_toml_files(path)
            if files == []:
                print(self.ld["view_file"]["noFiles"])
                await_retry(self.ld)
                continue
            else:
                break

        # Giving file list and getting option
        print(self.ld["view_file"]["fileList"])
        for file in files:
            print(file)
        break_line()
        file_to_view = questionary.select(
            "Select the file you would like to view:",
            choices=files
        ).ask()
        break_line()

        # Showing file
        file_contents = toml.load(path + file_to_view)["content"]
        clear()
        print(file_contents)
        break_line(3)
        await_enter(self.ld, to_exit=True)
        clear()

    def find_all_toml_files(self, path):
        files = []

        for element in os.listdir(path):
            print(element)
            if element.split(".")[-1] == "toml":
                if validate_key(toml.load(path + element)["randomized_key"]):
                    files.append(element)

        return files

