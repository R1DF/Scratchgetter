# Imports
from tools import *
import requests
import datetime
import questionary

# Constants
API_USER = "https://api.scratch.mit.edu/users/~/"

# UserProcess class
class UserProcess:
    def __init__(self, master):
        # Inheriting
        self.master = master
        self.ll = self.master.ll
        self.ld = self.master.ld

        # Beginning process
        self.begin_user_process()

    def format_date(self, details):
        # Sample variable: 2016-01-10T05:12:21.000Z
        formatted = ""

        # Formatting date
        date, time = details.split("T")
        year, month, day = date.split("-")
        month = {
            "01": "January",
            "02:": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }[month]

        if day[-1] == "1" and day != "11":
            ordinal = "st"
        elif day[-1] == "2" and day != "12":
            ordinal = "nd"
        elif day[-1] == "3" and day != "13":
            ordinal = "rd"
        else:
            ordinal = "th"

        formatted += f"{day}{ordinal} {month} {year} at "

        # Formatting time
        time = time[:8]  # Cutting off the ".XXXZ"
        formatted += time

        return formatted

    def get_user(self, profile):
        # Connecting to the API
        log("Connecting to the API...")
        response = requests.get(API_USER.replace("~", profile))
        print("Done.")

        # Loading data
        log("Unpacking data...")
        json_data = response.json()
        print("Done.")

        # Creating dictionary, loading ST status and username
        profile_data = {"username": json_data["username"]}
        log("Loading ST status...")
        profile_data["isST"] = json_data["scratchteam"]
        print("Done.")

        # Getting join date
        log("Loading join date...")
        profile_data["join_date"] = self.format_date(json_data["history"]["joined"])
        print("Done.")

        # Getting user ID
        log("Loading ID...")
        profile_data["userId"] = str(json_data["id"])
        print("Done.")

        # Delving into profile information, profile ID, loading status and bio
        log("Loading profile contents...")
        json_data = json_data["profile"]
        profile_data["profileId"] = str(json_data["id"])
        print("Done.")

        log("Loading \"About Me\" section...")
        profile_data["aboutMe"] = json_data["bio"]
        print("Done.")

        log("Loading \"What I'm Working On\" section...")
        profile_data["WIWO"] = json_data["status"]
        print("Done.")

        # Loading user's country
        log("Loading country...")
        profile_data["country"] = json_data["country"]
        print("Done.")

        # Loading images
        log("Loading profile picture links...")
        profile_data["iconLinks"] = json_data["images"]
        print("Done.")

        # Returning all content
        return profile_data

    def save_user(self, path, details, profile_picture_links):
        resolutions = ("90x90", "60x60", "55x55", "50x50", "32x32")
        with open(path + ".txt", "w") as f:
            f.write(details)
            f.write("\n\nProfile pictures links:\n")
            for resolution in range(len(resolutions)):
                f.write(f"{resolutions[resolution]}: {profile_picture_links[resolutions[resolution]]}\n")
            f.write(f"\n{str(datetime.datetime.now())}")

    def reveal_user(self, details):
        # Getting output
        output = open(os.getcwd() + "\\templates\\user.txt", "r").read()[29:]

        # Modifying template
        output = output.replace("USERNAME", details["username"])
        output = output.replace("IS_ST",
                       "The user is a member of the Scratch Team." if details[
                           "isST"] else "The user is not a member of the Scratch Team."
                       )
        output = output.replace("DATETIME", details["join_date"])
        output = output.replace("COUNTRY", details["country"])
        output = output.replace("PROFILE_ID", details["profileId"])
        output = output.replace("USER_ID", details["userId"])

        if details["aboutMe"].strip() == "":
            output = output.replace("ABOUT_ME", "The user's \"About Me\" section is empty.")
        else:
            output = output.replace("ABOUT_ME", f"About Me:\n{details['aboutMe']}")

        if details["WIWO"].strip() == "":
            output = output.replace("WIWO", "The user's \"What I'm Working On\" section is empty.")
        else:
            output = output.replace("WIWO", f"What I'm Working On:\n{details['WIWO']}")
        print(output)
        return output, details["iconLinks"]  # returns PFPs

    def begin_user_process(self):
        # Getting user input
        username = questionary.text(self.ld["get_user"]["enterUsername"], validate=lambda x: x.strip() != "").ask().strip()

        # Getting profile content
        clear()
        print(self.ld["get_user"]["enterUsername"], username)
        user_data = self.get_user(username)
        break_line()
        print(self.ld["get_user"]["userObtained"])
        await_enter()

        # Showing all content
        clear()
        formatted_response, profile_pictures = self.reveal_user(user_data)

        break_line()
        print("Images for the profile pictures are accessible in a text file.")
        should_save = questionary.select(
            "Would you like to save the text file?",
            choices=[
                "Yes",
                "No"
            ]
        ).ask()

        if should_save == "Yes":
            path = questionary.path("Enter file folder (Tab for hints):", only_directories=True,
                                    default=os.getcwd() + "\\saves\\").ask()
            file_name = questionary.text("Enter file name:", validate=lambda x: x.strip() != "",
                                         default=username).ask().strip()
            self.save_user(path + "\\" + file_name, formatted_response, profile_pictures)
            input("\nSuccess.\nHit Enter to exit the menu.\n")
        clear()

