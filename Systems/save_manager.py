#Other Modules
import json
import os


class SaveSystem:
    def __init__(self):
        self.file_extention = ".json"
        self.save_folder = "save_data"

    def save_data(self, data, name):
        with open("../"+self.save_folder+"/"+name+self.file_extention, "w") as f:
            json.dump(data, f, indent=3)

    def load_data(self, name):
        data_file = open(self.save_folder+"/"+name, "rb")
        data = json.load(data_file)
        return data

    def check_for_file(self, name):
        return os.path.exists("../"+self.save_folder+"/"+name+self.file_extention)
    
