from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
# stemming
from nltk.stem import PorterStemmer
import re
import os

from model import Model


class IRS:
    """This class has the propose of orchestrate the IRS process.
    """

    def __init__(self, path_to_index='./irs_data'):
        self.path_to_index = path_to_index
        self.models = {}

    def processing_text(self, raw_text: str, language: str) -> list[str]:
        """This method has the propose of processing the text
        Returns: a List of stemmed and normalized tokens
        """
        raw_text = re.sub(r'[^\w\s]', '', raw_text)
        res = tokenize(raw_text, language)
        stop_list = stopwords.words(language)
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in res if token not in stop_list]

    def add_model(self, model: Model):
        """This method add a model to the IRS

        Args:
            model (Model): This is a model of IRS like the Vector Space Model

        Raises:
            Exception: If the model is already in the IRS
        """
        assert isinstance(model, Model)
        if model.get_model_name() in self.models:
            raise Exception(
                f"A model with the same name as '{model.get_model_name()}' already exists in the system")
        self.models[model.get_model_name()] = model
        if not os.path.isdir(f'{self.path_to_index}/{model.get_model_name()}'):
            os.makedirs("path/to/demo_folder2")

    def get_model_storage_path(self, model_name: str) -> str:
        """This method returns the path to the storage of the model

        Args:{model_name}
            model_name (str): The name of the model

        Returns:
            str: The path to the storage of the model
        """
        if not os.path.isdir(f'{self.path_to_index}/{model_name}'):
            raise Exception(f'The storage folder for the model "{model_name}" does not exist')
        return f"{self.path_to_index}/{model_name}"
