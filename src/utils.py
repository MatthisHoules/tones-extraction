# External Imports
import os

def is_file_csv(file_path : str) -> bool : 
    """is_file_csv

        ### params :
            file_path : str
                file path to check if it's a csv file
        ### return
            False if file does not exist or if file isn't a csv file. Returns True instead
    """


    if not os.path.exists(file_path) or not os.path.isfile(file_path) :
        return False
        
    return os.path.splitext(file_path)[1].lower() == ".csv"
# def is_file_csv(file_path : str) -> boola