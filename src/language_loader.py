# Imports
import toml
import os

# Constants
PATH = os.getcwd() + "\\languages\\"
DEFAULT_LANGUAGE = toml.load(os.getcwd() + "\\conf.toml")["language"]

# Language loader class
class LanguageLoader:
    def __init__(self):
        self.default_language_path = PATH + DEFAULT_LANGUAGE
        self.data = toml.load(self.default_language_path)
        self.metadata = self.data["meta"]

