from src.document import Document
from typing import Callable
from src.storage import Storage

# TODO: Create a factory for creating models
class Model:
    def __init__(self, text_processor: Callable[[str, str], list[str]]):
        self.documents: dict[int, Document] = {}
        self.text_processor = text_processor

    def get_model_name(self) -> str:
        return self.__class__.__name__

    def add_documents(self, documents: list[Document]):
        pass

    def add_document(self, document: Document):
        """This method index the document according to an specific implementation of a model

        Args:
            document (Document | None): The document to be indexed
        """
        pass

    def get_ranking(self, query:str, first_n_results:int, lang:str = 'english') -> list[Document]:
        """Given a query this method returns the first n more relevant results

        Args:
            query (str): This is a string with the user information need a.k.a a query
            first_n_results (int): The amount of documents you want retrieved
            lang (str, optional): The language of the query. Defaults to 'english'.

        Returns:
            list[Document]: A list of documents sorted by relevance
        """
        return [x for x in self.documents.values()]
