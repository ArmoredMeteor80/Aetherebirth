import pickle
import os


class SaveLoadSystem:
    """Système de sauvegarde et de chargement"""
    def __init__(self, file_extension: str, save_folder: str):
        """Constructeur"""
        self.file_extension = file_extension
        self.save_folder = save_folder

    def save_data(self, data: any, name: str):
        """Sauvegarde les données"""
        data_file = open(self.save_folder+"/"+name+self.file_extension, "wb")
        pickle.dump(data, data_file)

    def load_data(self, name: str):
        """Charge les données"""
        data_file = open(self.save_folder+"/"+name+self.file_extension, "rb")
        data = pickle.load(data_file)
        return data

    def check_for_file(self, name: str):
        """Vérifie qu'une sauvegarde est déjà présente"""
        return os.path.exists(self.save_folder+"/"+name+self.file_extension)

    def load_game_data(self, files_to_load: list, default_data: list):
        """Charge toutes les données du jeu"""
        variables = []
        for index, file in enumerate(files_to_load):
            if self.check_for_file(file):
                variables.append(self.load_data(file))
            else:
                variables.append(default_data[index])

        if len(variables) > 1:
            return tuple(variables)
        else:
            return variables[0]

    def save_game_data(self, data_to_save: list, file_names: list):
        """Sauvegarde toutes les données du jeu"""
        for index, file in enumerate(data_to_save):
            self.save_data(file, file_names[index])
