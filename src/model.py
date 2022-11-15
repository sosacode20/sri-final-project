from document import Document
from irs import IRS

class Model:
    def __init__(self, irs):
        self.document = []
        self.irs = irs

    def get_model_name(self) -> str:
        return self.__class__.__name__

    def add_documents(self, documents):
        pass

    def add_document(self, document):
        pass

    def index_query(self, query):
        pass

    def get_sim(self, query):
        pass