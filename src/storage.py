import os

class Storage:
    """Class for handling all storage processes of an IRS
    """

    def __init__(self, path_to_index='./irs_data'):
        """Initialize a storage object looking for info in a root path

        Args:
            path_to_index (str, optional): This is the root directory where all the IRS models will store there info. Defaults to './irs_data'.
        """
        self.path_to_index = path_to_index
    
    def get_storage_path(self, name: str) -> str:
        """This method returns the path to a specific storage. Useful for IRS models

        Args:
            name (str): The name of the storage. In the case of an IRS model is the model name

        Raises:
            Exception: If the directory doesn't exists

        Returns:
            str: The path to the storage
        """
        if not os.path.isdir(f'{self.path_to_index}/{name}'):
            raise Exception(f'The storage folder for the model "{name}" does not exist')
        return f"{self.path_to_index}/{name}"
    
    def create_storage_path(self, name: str):
        """This method create a new storage directory with the given name

        Args:
            name (str): Name of the new storage path
        """
        path = f'{self.path_to_index}/{name}'
        if not os.path.isdir(path):
            os.makedirs(path)
