from src.model import Model
from src.storage import Storage
from src.irs_parser import Parser
from src.utils import get_all_files_with_extension
from src.document import Document

class IRS:
    """This class has the propose of orchestrate the IRS process.
    """

    def __init__(self, storage: Storage):
        self.storage = storage
        self.models: dict[str, Model] = {}
        self.parsers: dict[str, Parser] = {}

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
        if self.storage.model_exists(model.get_model_name()):
            model = self.storage.load_model(model.get_model_name())
        self.models[model.get_model_name()] = model

    def list_models(self) -> list[str]:
        """Returns the name of the models loaded for the system

        Returns:
            list[str]: List with the names of the stored models
        """
        return sorted(self.models.keys())

    def add_parser(self, parser:Parser):
        """Add a new Parser to the IRS. Note that two different parsers with the same 'pretty_name' will be recognized as the same

        Args:
            parser (Parser): A new parser to add to the system

        Raises:
            Exception: It's raised if the parser was already added to the system
        """
        # TODO: Debate if we should remove the exception and simply override with the new parser
        parser_name = parser.get_pretty_name()
        if parser_name in self.parsers:
            raise Exception(f"The parser with name {parser_name} it's already loaded")
        self.parsers[parser_name] = parser

    def list_parsers(self) -> list[str]:
        """Returns all the names of the parsers loaded in the system

        Returns:
            list[str]: The sorted list with the names of the parsers in the system
        """
        return sorted(self.parsers.keys())

    def add_document(self, document:Document):
        for model in self.models.values():
            model.add_document(document)

    def add_document_collection(self, path:str, parser_name:str, model_name:str):
        """Adds a collection of documents to the system

        Args:
            path (str): This is the root path from where to start the search for files that the parser given can parse
            parser_name (str): The name of the parser in the system that will parse the collections
            model_name (str): The name of the model in the system that will index the documents

        Raises:
            Exception: If the parser is not in the system
            Exception: If the model is not in the system
        """
        if parser_name not in self.parsers:
            raise Exception(f'The parser with name {parser_name} it\'s not loaded in the system')
        if model_name not in self.models:
            raise Exception(f'The model with name {model_name} it\'s not loaded in the system')
        parser = self.parsers[parser_name]
        model = self.models[model_name]
        all_files = get_all_files_with_extension(path, parser.get_extension_list())
        for file_path in all_files:
            with open(file_path, 'r') as file:
                documents = parser.parse(file)
                for document in documents:
                    model.add_document(document)

    def get_ranking(self, query:str, model_name:str, first_n_results:int):
        if model_name not in self.models:
            raise Exception(f'The model with name {model_name} it\'s not loaded in the system')
        model = self.models[model_name]
        return [(doc.doc_id, doc.doc_name) for doc in model.get_ranking(query, first_n_results)]

    def save(self):
        for model in self.models.values():
            self.storage.save_model(model.get_model_name(), model)
