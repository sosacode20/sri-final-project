from model import Model
from storage import Storage
from parser import Parser
from utils import get_all_files_with_extension
from document import Document

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
        self.models[model.get_model_name()] = model
        self.storage.create_storage_path(model.get_model_name())

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
                # match document:
                #     case Document(_,_,_,_,_):
                #         model.add_document(document)
                #     case [Document(_,_,_,_,_), *rest]:
                #         for doc in document:
                #             model.add_document(doc)
                #     case None:
                #         print(f'Error parsing file {file_path}')
                # model.add_document(document)

    def get_ranking(self, query:str, model_name:str, first_n_results:int):
        if model_name not in self.models:
            raise Exception(f'The model with name {model_name} it\'s not loaded in the system')
        model = self.models[model_name]
        return [x.doc_name for x in model.get_ranking(query, first_n_results)]

