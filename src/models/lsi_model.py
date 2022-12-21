# - lsi_model
# - evaluation
# - report
# - fixes




from src.model import Model
from typing import Callable
# from ..document import Document
from src.document import Document
import numpy as np
import math
import random

class LSI_Model(Model):
    def __init__(self, text_preprocessor: Callable[[str, str], list[str]]):
        super().__init__(text_preprocessor)
        self.dirty = 0
        self.tf: dict[tuple[str, int], float] = {}
        self.df: dict[str, int] = {}
        self.tf_idf = None

        self.term_doc_matrix = None

    def get_name(self):
        return "LSI_Model"

    def add_document(self, document: Document):
        # tell the model that needs to recalculate the vectors of documents
        self.dirty = 1
        self.documents.append(document)
        title = document.doc_normalized_name
        body = document.doc_normalized_body
        text = title + body
        term_frequency = self._get_tf(text)
        # Add the document to the list of documents
        # Update the amount of documents in which the term is
        for token in term_frequency:
            if token in self.df:
                self.df[token] += 1
            else:
                self.df[token] = 1
            self.tf[(token, len(self.documents) - 1)] = term_frequency[token]

    def _get_tf(self, text: list[str]) -> dict[str, float]:
        tf: dict[str, float] = { }
        
        max_frequency = 0
        for token in text:
            if token in tf:
                tf[token] += 1
            else:
                tf[token] = 1
            if tf[token] > max_frequency:
                max_frequency = tf[token]
        for token in tf:
            tf[token] = tf[token] / max_frequency
        return tf

    def _dimension_reduction(self):
        k = [ 100, 200, 300]
        r = random.randint(0, 2)
        return k[r]

    def _query_dimension_reduction(self, U, S):
        query_vector = np.dot(np.dot(np.linalg.inv(S),U.transpose()),self.query_vector)
        query_vector = np.round(query_vector,4)
        return query_vector

    def apply_svd(self):
        U, S, VT = np.linalg.svd(self.term_doc_matrix)
        U = np.round(U,4)
        S = np.round(S,4)
        S = np.diag(S)
        VT = np.round(VT,4)

        k = self._dimension_reduction()
        rows = len(self.term_doc_matrix)
        columns = len(self.term_doc_matrix[0])
        U2 = U[ : rows, : k]
        S2 = S[0 : k]
        VT2 = VT[ : k, : columns]

        return U2, S2, VT2

    #TODO: Review this
    def generate_term_doc_matrix(self):
        self.term_doc_matrix = np.zeros((len(self.df), len(self.documents)))
        for token in self.df:
            for i in range(len(self.documents)):
                if (token, i) in self.tf:
                    #tf-idf
                    self.term_doc_matrix[self.df[token], i] = self.tf[(token, i)] * math.log(len(self.documents) / self.df[token])
        self.dirty = 0

    def get_ranking(self, query: str, first_n_results: int, offset: int, lang: str = 'english') -> list[tuple[Document, float]]:
        if self.dirty:
            self.generate_term_doc_matrix()
        U, S, Vt = self.apply_svd()
        query_vector = self.make_query_vector
        query_vector = self._query_dimension_reduction(U, S)

        ##
        score = 0
        rank = {}
        ##
        for i in range(len(Vt[0])):
            doc_column = Vt[:, i:i + 1]
            score = np.round(self.similarity(doc_column, query_vector), 4)
            doc_name = self.documents[i]
            rank[doc_name:score]
        result = dict(sorted(rank.items(), key = lambda item: item[1], reverse=True))
        return result