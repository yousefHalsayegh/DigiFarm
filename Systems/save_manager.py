#Other Modules
import json
import os


class SaveSystem:
    def __init__(self):
        """
        A class used to save the game state 
        """
        self.save_folder = "save_data"


    def save_data(self, data, name):
        """
        Used to write the current state of the game into a JSON file
        # Parameters
        **data** : _Dict_ \n
        This contians the general information and specific information of each digimon 
        **name** : _str_ \n 
        The file name which the data will be saved in 
        """
        #opens a file either new or exsiting and write in it the JSON
        with open(self.save_folder+"/"+name+".json", "w") as f:
            #turns the dict to JSON and dump it all inside the file, the indent 3 is just for style 
            json.dump(data, f, indent=3)

    def load_data(self, name):
        """
        Used to read the data inside the file and restore the current state of the game 
        # Parameter:
        **name** : _str_ \n
        The file name which contains the data 
        # Return 
        **data** : _Dict_ \n
        The data present inside the file to restore the game state
        """
        #retrive the information inside the file
        data_file = open(self.save_folder+"/"+name, "rb")
        #extract the infromatioin inside the file
        data = json.load(data_file)
        return data
    def files (self):
        """
        Lists all the files inside a folder
        # Return 
        **dir** : _list_ \n
        The names of each file inside the folder
        """
        return os.listdir(self.save_folder)
    def delete(self, name):
        """
        Delete a specific file 
        # Parameter
        **name** : _str_ \n 
        The file name you want to delete 
        """
        os.remove(self.save_folder+"/"+name)

