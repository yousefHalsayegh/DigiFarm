#Other Modules
import pickle
import os


class SaveSystem:
    def __init__(self, file_extension, save_folder):
        self.file_extention = file_extension
        self.save_folder = save_folder

    def save_data(self, data, name):
        data_file = open("../"+self.save_folder+"/"+name+self.file_extention, "wb")
        pickle.dump(data, data_file)

    def load_data(self, name):
        data_file = open("../"+self.save_folder+"/"+name, "rb")
        data = pickle.load(data_file)
        return data

    def check_for_file(self, name):
        return os.path.exists("../"+self.save_folder+"/"+name+self.file_extention)
    
