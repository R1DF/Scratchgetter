# Imports
from tools import *
import requests
import datetime
import questionary
import importlib
import toml

# Constants
API_STUDIO = "https://api.scratch.mit.edu/studios/~/"


# StudioProcess class
class StudioProcess:
    def __init__(self, master):
        # Inheriting
        self.master = master
        self.ll = self.master.ll
        self.ld = self.master.ld

        # Getting date formatter
        self.format_date = importlib.import_module(f"{self.ld['linked']['dateFormatterFile']}").format_date

        # Beginning process
        self.begin_studio_process()

    def save_studio(self, path, details, thumbnail):
        toml.dump({
            "randomized_key": randomize_key(),
            "content": f"{details}\n\n{self.ld['get_studio']['thumbnailLink']}\n{thumbnail}\n\n{str(datetime.datetime.now())}"
        }, open(path + ".toml", "w", encoding="utf-8"))


    def reveal_studio(self, details):
        # Getting output from template
        output = self.ld["templates"]["studio"]

        output = output.replace(
            "STUDIO_ID", str(details["studio_id"])
        ).replace(
            "HOST_ID", str(details["host_id"])
        ).replace(
            "COMMENTS", str(details["comments"])
        ).replace(
            "FOLLOWERS", str(details["followers"])
        ).replace(
            "MANAGERS", str(details["managers"])
        ).replace(
            "PROJECTS", str(details["projects"])
        ).replace(
            "DATE_CREATED", details["creation_date"]
        ).replace(
            "DATE_LAST_EDITED", details["last_edited_date"]
        ).replace(
            "DATE_CREATED", details["creation_date"]
        ).replace(
            "DATE_LAST_EDITED", details["last_edited_date"]
        ).replace(
            "DESCRIPTION", f"{self.ld['get_studio']['hasDescriptionReplacer']}\n{details['description']}" if details[
                                                                                                                  "description"].strip() != "" else
            self.ld["get_studio"]["noDescriptionReplacer"]
        ).replace(
            "ALLOWS_COMMENTING",
            self.ld["get_studio"]["hasCommentsReplacer"] if details["has_comments"] else self.ld["get_studio"][
                "noCommentsReplacer"]
        ).replace(
            "ALLOWS_ANY_PROJECT",
            self.ld["get_studio"]["allowsAnyProjectsReplacer"] if details["is_open"] else self.ld["get_studio"][
                "forbidsAnyProjectsReplacer"]
        )

        print(output)
        return output, details["thumbnail"]  # returns thumbnails too for later use

    def get_studio(self, studio_id):
        # Connecting to the API
        log(self.ld["reusable"]["connectingToAPIAwaiter"])
        response = requests.get(API_STUDIO.replace("~", studio_id))
        insert_success(self.ld)

        # Loading data
        log(self.ld["reusable"]["collectingDataAwaiter"])
        json_data = response.json()
        insert_success(self.ld)

        # Checking if the user exists
        log("Validating studio existence...")
        try:
            json_data["id"]  # 404 responses do not have IDs
        except KeyError:
            return None

        # Creating dictionary, loading title
        studio_data = {"studio_id": json_data["id"]}
        log(self.ld["get_studio"]["loadingTitleAwaiter"])
        studio_data["name"] = json_data["title"]
        insert_success(self.ld)

        # Getting host ID
        log(self.ld["get_studio"]["loadingHostIDAwaiter"])
        studio_data["host_id"] = json_data["host"]
        insert_success(self.ld)

        # Getting description
        log(self.ld["get_studio"]["loadingDescriptionAwaiter"])
        studio_data["description"] = json_data["description"]
        insert_success(self.ld)

        # Determining if comments are allowed
        log(self.ld["get_studio"]["loadingHasCommentsAwaiter"])
        studio_data["has_comments"] = json_data["comments_allowed"]
        insert_success(self.ld)

        # Determining if adding any projects is allowed
        log(self.ld["get_studio"]["loadingIsOpenAwaiter"])
        studio_data["is_open"] = json_data["open_to_all"]
        insert_success(self.ld)

        # Getting studio stats
        log(self.ld["get_studio"]["loadingCommentsAwaiter"])
        studio_data["comments"] = json_data["stats"]["comments"]
        insert_success(self.ld)

        log(self.ld["get_studio"]["loadingFollowersAwaiter"])
        studio_data["followers"] = json_data["stats"]["followers"]
        insert_success(self.ld)

        log(self.ld["get_studio"]["loadingManagersAwaiter"])
        studio_data["managers"] = json_data["stats"]["managers"]
        insert_success(self.ld)

        log(self.ld["get_studio"]["loadingProjectsAwaiter"])
        studio_data["projects"] = json_data["stats"]["projects"]
        insert_success(self.ld)

        # Getting dates
        log(self.ld["get_studio"]["loadingCreationDateAwaiter"])
        studio_data["creation_date"] = self.format_date(json_data["history"]["created"], self.ld)
        insert_success(self.ld)

        log(self.ld["get_studio"]["loadingEditDateAwaiter"])
        studio_data["last_edited_date"] = self.format_date(json_data["history"]["modified"], self.ld)
        insert_success(self.ld)

        # Getting thumbnail
        log(self.ld["get_studio"]["loadingThumbnailAwaiter"])
        studio_data["thumbnail"] = json_data["image"]
        insert_success(self.ld)

        # Returning all data
        return studio_data

    def begin_studio_process(self):
        # Getting user input
        studio_id = questionary.text(self.ld["get_studio"]["enterStudioIDQuery"],
                                      validate=lambda x: x.isnumeric()).ask().strip()

        # Getting project content
        clear()
        print(self.ld["get_studio"]["studioID"], studio_id)
        studio_data = self.get_studio(studio_id)

        # Checking if the project actually exists
        if studio_data is None:
            insert_error(self.ld)
            print(self.ld["get_studio"]["studioInexistent"].replace("STUDIO_ID", studio_id))
            await_enter(self.ld, to_exit=True)
            clear()
            return

        # Showing all content
        clear()
        formatted_response, thumbnails = self.reveal_studio(studio_data)

        # File saving option
        print(self.ld["get_studio"]["thumbnailAvailability"])
        should_save = questionary.select(
            self.ld["reusable"]["saveFileQuery"],
            choices=[
                self.ld["reusable"]["yes"],
                self.ld["reusable"]["no"]
            ]
        ).ask()

        if should_save == self.ld["reusable"]["yes"]:
            path = questionary.path(self.ld["reusable"]["enterFileFolderQuery"], only_directories=True,
                                    default=os.getcwd() + "\\saves\\studios\\").ask()
            file_name = questionary.text(self.ld["reusable"]["enterFileNameQuery"], validate=lambda x: x.strip() != "",
                                         default=f"studio_{studio_id}").ask().strip()
            self.save_studio(path + "\\" + file_name, formatted_response, thumbnails)
            print(self.ld["reusable"]["success"])
            await_enter(self.ld, to_exit=True)
        clear()

