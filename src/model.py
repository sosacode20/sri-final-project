from src.document import Document
from typing import Callable

# TODO: Create a factory for creating models
class Model:
    def __init__(self, text_processor: Callable[[str, str], list[str]]):
        self.documents: list[Document] = []
        self.text_processor = text_processor

    def get_name(self) -> str:
        return self.__class__.__name__

    def add_document(self, document: Document):
        """This method index the document according to an specific implementation of a model

        Args:
            document (Document | None): The document to be indexed
        """
        pass

    def get_ranking(self, query:str, first_n_results:int, offset:int, lang:str = 'english') -> list[tuple[Document, float]]:
        """Given a query this method returns the first n more relevant results

        Args:
            query (str): This is a string with the user information need a.k.a a query
            first_n_results (int): The amount of documents you want retrieved
            lang (str, optional): The language of the query. Defaults to 'english'.

        Returns:
            list[Document]: A list of documents sorted by relevance
        """
        return [x for x in self.documents]

    def _get_document_by_id(self, documents:list[Document], id:int, start:int, end:int) -> Document:
        if start > end:
            return None
        mid = (start + end) // 2
        if documents[mid].doc_id == id:
            return documents[mid]
        elif documents[mid].doc_id < id:
            return self._get_document_by_id(documents, id, mid + 1, end)
        else:
            return self._get_document_by_id(documents, id, start, mid - 1)

    #TODO: remake this method with binary search
    def get_document_by_id(self, id:int) -> Document:
        return self._get_document_by_id(self.documents, id, 0, len(self.documents) - 1)
