# Imports
from tools import *
import requests
import datetime
import questionary
import importlib
import toml

# Constants
API_USER = "https://api.scratch.mit.edu/users/~/"


# UserProcess class
class UserProcess:
    def __init__(self, master):
        # Inheriting
        self.master = master
        self.ll = self.master.ll
        self.ld = self.master.ld

        # Getting date formatter
        self.format_date = importlib.import_module(f"{self.ld['linked']['dateFormatterFile']}").format_date

        # Beginning process
        self.begin_user_process()

    def get_user(self, profile):
        # Connecting to the API
        log(self.ld["reusable"]["connectingToAPIAwaiter"])
        response = requests.get(API_USER.replace("~", profile))
        insert_success(self.ld)


        # Loading data
        log(self.ld["reusable"]["collectingDataAwaiter"])
        json_data = response.json()
        insert_success(self.ld)

        # Checking if the user exists
        log("Validating user existence...")
        try:
            json_data["id"]  # 404 responses do not have IDs
        except KeyError:
            return None
        insert_success(self.ld)

        # Creating dictionary, loading ST status and username
        profile_data = {"username": json_data["username"]}
        log(self.ld["get_user"]["loadingSTStatusAwaiter"])
        profile_data["isST"] = json_data["scratchteam"]
        insert_success(self.ld)

        # Getting join date
        log(self.ld["get_user"]["loadingJoinDateAwaiter"])
        profile_data["join_date"] = self.format_date(json_data["history"]["joined"], self.ld)
        insert_success(self.ld)

        # Getting user ID
        log(self.ld["get_user"]["loadingIDAwaiter"])
        profile_data["userId"] = str(json_data["id"])
        insert_success(self.ld)

        # Delving into profile information, profile ID, loading status and bio
        log(self.ld["get_user"]["loadingProfileContentsAwaiter"])
        json_data = json_data["profile"]
        profile_data["profileId"] = str(json_data["id"])
        insert_success(self.ld)

        log(self.ld["get_user"]["loadingAboutMeAwaiter"])
        profile_data["aboutMe"] = json_data["bio"]
        insert_success(self.ld)

        log(self.ld["get_user"]["loadingWIWOAwaiter"])
        profile_data["WIWO"] = json_data["status"]
        insert_success(self.ld)

        # Loading user's country
        log(self.ld["get_user"]["loadingCountryAwaiter"])
        profile_data["country"] = json_data["country"]
        insert_success(self.ld)

        # Loading images
        log(self.ld["get_user"]["loadingPFPLinksAwaiter"])
        profile_data["iconLinks"] = json_data["images"]
        insert_success(self.ld)

        # Returning all content
        return profile_data

    def save_user(self, path, details, profile_picture_links):
        content = details + f"\n\n{self.ld['get_user']['PFPLinks']}\n"

        resolutions = ("90x90", "60x60", "55x55", "50x50", "32x32")
        for resolution in range(len(resolutions)):
            content += f"{resolutions[resolution]}: {profile_picture_links[resolutions[resolution]]}\n"
        content += f"\n{str(datetime.datetime.now())}"

        toml.dump({
            "randomized_key": randomize_key(),
            "content": content
        }, open(path + ".toml", "w", encoding="utf-8"))

    def reveal_user(self, details):
        # Getting output from template
        output = self.ld["templates"]["user"]

        # Modifying template
        output = output.replace("USERNAME", details["username"])
        output = output.replace("IS_ST",
                                self.ld["get_user"]["isSTReplacer"] if details[
                                    "isST"] else self.ld["get_user"]["notSTReplacer"]
                                )
        output = output.replace("DATETIME", details["join_date"])
        output = output.replace("COUNTRY", details["country"])
        output = output.replace("PROFILE_ID", details["profileId"])
        output = output.replace("USER_ID", details["userId"])

        if details["aboutMe"].strip() == "":
            output = output.replace("ABOUT_ME", self.ld["get_user"]["noAboutMeReplacer"])
        else:
            output = output.replace("ABOUT_ME", f"{self.ld['get_user']['hasAboutMeReplacer']}\n{details['aboutMe']}")

        if details["WIWO"].strip() == "":
            output = output.replace("WIWO", self.ld["get_user"]["noWIWOReplacer"])
        else:
            output = output.replace("WIWO", f"{self.ld['get_user']['hasWIWOReplacer']}\n{details['WIWO']}")
        print(output)
        return output, details["iconLinks"]  # returns PFPs too for later use

    def begin_user_process(self):
        # Getting user input
        username = questionary.text(self.ld["get_user"]["enterUsernameQuery"],
                                    validate=lambda x: x.strip() != "").ask().strip()

        # Getting profile content
        clear()
        print(self.ld["get_user"]["user"], username)
        user_data = self.get_user(username)

        # Checking if profile even exists
        if user_data is None:
            insert_error(self.ld)
            print(self.ld["get_user"]["userInexistent"].replace("USERNAME", username))
            await_enter(self.ld, to_exit=True)
            clear()
            return

        break_line()
        print(self.ld["get_user"]["userObtained"])
        await_enter(self.ld)

        # Showing all content
        clear()
        formatted_response, profile_pictures = self.reveal_user(user_data)

        # File saving option
        print(self.ld["get_user"]["imageAvailability"])
        should_save = questionary.select(
            self.ld["reusable"]["saveFileQuery"],
            choices=[
                self.ld["reusable"]["yes"],
                self.ld["reusable"]["no"]
            ]
        ).ask()

        if should_save == self.ld["reusable"]["yes"]:
            path = questionary.path(self.ld["reusable"]["enterFileFolderQuery"], only_directories=True,
                                    default=os.getcwd() + "\\saves\\users\\").ask()
            file_name = questionary.text(self.ld["reusable"]["enterFileNameQuery"], validate=lambda x: x.strip() != "",
                                         default=username).ask().strip()
            self.save_user(path + "\\" + file_name, formatted_response, profile_pictures)
            print(self.ld["reusable"]["success"])
            await_enter(self.ld, to_exit=True)
        clear()
