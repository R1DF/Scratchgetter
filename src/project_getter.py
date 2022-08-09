# Imports
from tools import *
import requests
import datetime
import questionary
import importlib

# Constants
API_PROJECT = "https://api.scratch.mit.edu/projects/~/"


# ProjectProcess class
class ProjectProcess:
    def __init__(self, master):
        # Inheriting
        self.master = master
        self.ll = self.master.ll
        self.ld = self.master.ld

        # Getting date formatter
        self.format_date = importlib.import_module(f"{self.ld['linked']['dateFormatterFile']}").format_date

        # Beginning process
        self.begin_project_process()

    def save_project(self, path, details, thumbnails):
        resolutions = ("480x360", "282x218", "216x163", "200x200", "144x108", "135x102", "100x80")
        with open(path + ".txt", encoding="utf-8", mode="w") as f:
            f.write(details)
            f.write(f"\n\n{self.ld['get_project']['thumbnailLinks']}\n")
            for resolution in range(len(resolutions)):
                f.write(f"{resolutions[resolution]}: {thumbnails[resolutions[resolution]]}\n")
            f.write(f"\n{str(datetime.datetime.now())}")

    def reveal_project(self, details):
        # Getting output from template
        output = self.ld["templates"]["project"]

        output = output.replace(
            "PROJECT_ID", str(details["project_id"])
        ).replace(
            "TITLE", details["title"]
        ).replace(
            "AUTHOR", details["author"]
        ).replace(
            "PROJECT_TOKEN", details["token"]
        ).replace(
            "IS_REMIX", self.ld["get_project"]["notRemixReplacer"] if not details["isRemix"] else self.ld["get_project"]["isRemixReplacer"].replace("PARENT_ID", str(details["parentID"])).replace("ROOT_ID", str(details["rootID"]))
        ).replace(
            "DATE_CREATED", details["creationDate"]
        ).replace(
            "DATE_LAST_EDITED", details["lastEditedDate"]
        ).replace(
            "DATE_PUBLISHED", details["lastPublishedDate"]
        ).replace(
            "VIEWS", str(details["views"])
        ).replace(
            "LOVES", str(details["loves"])
        ).replace(
            "FAVOURITES", str(details["faves"])
        ).replace(
            "REMIXES", str(details["remixes"])
        ).replace(
            "INSTRUCTIONS", f"{self.ld['get_project']['hasInstructionsReplacer']}\n{details['instructions']}" if details["instructions"].strip() != "" else self.ld["get_project"]["noInstructionsReplacer"]
        ).replace(
            "DESCRIPTION", f"{self.ld['get_project']['hasDescriptionReplacer']}\n{details['description']}" if details["description"].strip() != "" else self.ld["get_project"]["noDescriptionReplacer"]
        ).replace(
            "HAS_COMMENTS", self.ld["get_project"]["hasCommentsReplacer"] if details["hasComments"] else self.ld["get_project"]["noCommentsReplacer"]
        )

        print(output)
        return output, details["thumbnails"]  # returns thumbnails too for later use

    def get_project(self, project_id):
        # Connecting to the API
        log(self.ld["reusable"]["connectingToAPIAwaiter"])
        response = requests.get(API_PROJECT.replace("~", project_id))
        insert_success(self.ld)

        # Loading data
        log(self.ld["reusable"]["collectingDataAwaiter"])
        json_data = response.json()
        insert_success(self.ld)

        # Checking if the user exists
        log("Validating project existence...")
        try:
            json_data["id"]  # 404 responses do not have IDs
        except KeyError:
            return None

        # Creating dictionary, loading title
        project_data = {"project_id": json_data["id"]}
        log(self.ld["get_project"]["loadingTitleAwaiter"])
        project_data["title"] = json_data["title"]
        insert_success(self.ld)

        # Loading visibility
        log(self.ld["get_project"]["loadingVisibilityAwaiter"])
        project_data["visibility"] = json_data["is_published"]  # check to see the other options
        insert_success(self.ld)

        # Determining if the project is a remix
        log(self.ld["get_project"]["loadingIsRemixAwaiter"])
        if json_data["remix"]["parent"] is not None:
            project_data["isRemix"] = True
            project_data["parentID"] = json_data["remix"]["parent"]
            project_data["rootID"] = json_data["remix"]["root"]
        else:
            project_data["isRemix"] = False
        insert_success(self.ld)

        # Loading author
        log(self.ld["get_project"]["loadingAuthorAwaiter"])
        project_data["author"] = json_data["author"]["username"]
        insert_success(self.ld)

        # Loading token
        log(self.ld["get_project"]["loadingTokenAwaiter"])
        project_data["token"] = json_data["project_token"]
        insert_success(self.ld)

        # Loading dates
        log(self.ld["get_project"]["loadingCreationDateAwaiter"])
        project_data["creationDate"] = self.format_date(json_data["history"]["created"], self.ld)
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingEditDateAwaiter"])
        project_data["lastEditedDate"] = self.format_date(json_data["history"]["modified"], self.ld)
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingPublishDateAwaiter"])
        project_data["lastPublishedDate"] = self.format_date(json_data["history"]["shared"],
                                                             self.ld)  # Some unpublished projects may not have valid info
        insert_success(self.ld)

        # Loading stats
        log(self.ld["get_project"]["loadingViewsAwaiter"])
        project_data["views"] = json_data["stats"]["views"]
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingLovesAwaiter"])
        project_data["loves"] = json_data["stats"]["loves"]
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingFavouritesAwaiter"])
        project_data["faves"] = json_data["stats"]["favorites"]  # UK English > US English no cap
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingRemixesAwaiter"])
        project_data["remixes"] = json_data["stats"]["remixes"]
        insert_success(self.ld)

        # Loading instructions and description (lengthy parts)
        log(self.ld["get_project"]["loadingInstructionsAwaiter"])
        project_data["instructions"] = json_data["instructions"]
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingDescriptionAwaiter"])
        project_data["description"] = json_data["description"]
        insert_success(self.ld)

        # Finally
        log(self.ld["get_project"]["loadingHasCommentsAwaiter"])
        project_data["hasComments"] = json_data["comments_allowed"]
        insert_success(self.ld)

        log(self.ld["get_project"]["loadingThumbnailsAwaiter"])
        project_data["thumbnails"] = {"480x360": json_data["image"], **json_data["images"]}
        insert_success(self.ld)

        # Returning all data
        return project_data

    def begin_project_process(self):
        # Getting user input
        project_id = questionary.text(self.ld["get_project"]["enterProjectIDQuery"],
                                      validate=lambda x: x.isnumeric()).ask().strip()

        # Getting project content
        clear()
        print(self.ld["get_project"]["projectID"], project_id)
        project_data = self.get_project(project_id)

        # Checking if the project actually exists
        if project_data is None:
            insert_error(self.ld)
            print(self.ld["get_project"]["projectInexistent"].replace("PROJECT_ID", project_id))
            await_enter(self.ld, to_exit=True)
            clear()
            return

        # Showing all content
        clear()
        formatted_response, thumbnails = self.reveal_project(project_data)

        # File saving option
        print(self.ld["get_project"]["thumbnailAvailability"])
        should_save = questionary.select(
            self.ld["reusable"]["saveFileQuery"],
            choices=[
                self.ld["reusable"]["yes"],
                self.ld["reusable"]["no"]
            ]
        ).ask()

        if should_save == self.ld["reusable"]["yes"]:
            path = questionary.path(self.ld["reusable"]["enterFileFolderQuery"], only_directories=True,
                                    default=os.getcwd() + "\\saves\\").ask()
            file_name = questionary.text(self.ld["reusable"]["enterFileNameQuery"], validate=lambda x: x.strip() != "",
                                         default=f"project_{project_id}").ask().strip()
            self.save_project(path + "\\" + file_name, formatted_response, thumbnails)
            print(self.ld["reusable"]["success"])
            await_enter(self.ld, to_exit=True)
        clear()
