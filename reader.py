from os import path
from json import load, dump

class user(object):     #Object for s uer
    def __init__(self, username):       
        self.file = f".\\saves\\{username}.json"
        self.read()

    def read(self):     #Read from the user's json file
        if path.exists(self.file):
            with open(self.file) as f:
                self.data = load(f)

    def save(self):     #Write the user's current location to the json file
        with open(self.file, "w") as f:
            dump(self.data, f, indent=4)

    def location(self):
        return self.data["location"]


class world(object):    #Object for a world
    def __init__(self, name):
        self.file = f".\\worlds\\{name}.json"
        self.read()

    def read(self):
        if path.exists(self.file):
            with open(self.file) as f:
                self.data = load(f)

    def message(self, location):
        return self.data[location]["message"]        

    def options(self, location):
        return self.data[location]["options"]

    def locations(self, location):
        return self.data[location]["locations"]