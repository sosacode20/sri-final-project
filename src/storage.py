import os
from src.model import Model
import pickle

class Storage:
    """Class for handling all storage processes of an IRS
    """

    def __init__(self, path_to_index='./irs_data'):
        """Initialize a storage object looking for info in a root path

        Args:
            path_to_index (str, optional): This is the root directory where all the IRS models will store there info. Defaults to './irs_data'.
        """
        self.path_to_index = path_to_index
    
    def get_storage_path(self, name: str) -> tuple[bool,str]:
        """This method returns the path to a specific storage. Useful for IRS models
        INFO: This method is for future optimizations in the storage process. Not for now

        Args:
            name (str): The name of the storage. In the case of an IRS model is the model name

        Returns:
            str: The path to the storage
        """
        if not os.path.isdir(f'{self.path_to_index}/{name}'):
            return False, f'{self.path_to_index}/{name}'
        return True, f"{self.path_to_index}/{name}"
    
    def create_storage_path(self, name: str):
        """This method create a new storage directory with the given name.
        INFO: This method is for future optimizations in the storage process. Not for now

        Args:
            name (str): Name of the new storage path
        """
        path = f'{self.path_to_index}/{name}'
        if not os.path.isdir(path):
            os.makedirs(path)

    def save_model(self, name: str, obj: Model):
        """This method saves an object in a specific storage

        Args:
            name (str): The name of the storage
            obj (object): The object to be saved
        """
        with open(f'{self.path_to_index}/{name}.pkl', 'wb') as f:
            pickle.dump(obj, f)

    def load_model(self, name: str) -> Model:
        """This method loads an object from a specific storage

        Args:
            name (str): The name of the storage

        Returns:
            object: The object loaded from the storage
        """
        # Check if the file exists
        if not self.model_exists(name):
            raise Exception(f"The file {name}.pkl doesn't exists")
        with open(f'{self.path_to_index}/{name}.pkl', 'rb') as f:
            return pickle.load(f)

    def model_exists(self, name: str) -> bool:
        """This method checks if a model exists in the storage

        Args:
            name (str): The name of the model

        Returns:
            bool: True if the model exists, False otherwise
        """
        return os.path.isfile(f'{self.path_to_index}/{name}.pkl')
