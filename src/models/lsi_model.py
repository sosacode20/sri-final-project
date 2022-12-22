# - lsi_model
# - evaluation
# - report
# - fixes




from unittest import result
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
        self.dirty : bool = False
        self.tf: dict[tuple[str, int], float] = {}
        self.df: dict[str, int] = {}
        self.tf_idf = None

        self.term_doc_matrix = None

    def get_name(self):
        return "LSI_Model"

    def add_document(self, document: Document):
        # tell the model that needs to recalculate the vectors of documents
        self.dirty = True
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

    def _query_dimension_reduction(self, U, S, query_vector):
        Si = np.linalg.inv(S)
        Ut = U.transpose()
        a = np.dot(Si,Ut)
        query_vector = np.dot(a,query_vector)
        query_vector = np.round(query_vector,4)
        return query_vector

    def apply_svd(self):
        # cache this
        U, S, VT = np.linalg.svd(self.term_doc_matrix)
        U = np.round(U,4)
        S = np.round(S,4)
        S = np.diag(S)
        VT = np.round(VT,4)

        k = self._dimension_reduction()
        rows = len(self.term_doc_matrix)
        columns = len(self.term_doc_matrix[0])
        U2 = U[ : rows, : k]
        S2 = S[0 : k, 0 : k]
        VT2 = VT[ : k, : columns]

        return U2, S2, VT2

    #TODO: Review this
    def generate_term_doc_matrix(self):
        if not self.dirty:
            return
        self.term_doc_matrix = np.zeros((len(self.df), len(self.documents)))
        for i, token in enumerate(self.df):
            for j in range(len(self.documents)):
                if (token, j) in self.tf:
                    #tf-idf
                    self.term_doc_matrix[i, j] = self.tf[(token, j)] * math.log(len(self.documents) / self.df[token])
        self.U, self.S, self.Vt = self.apply_svd()
        self.dirty = False

    #TODO: Review this
    def generate_query_vector(self, query: str, lang: str = 'english'):
        query = self.text_processor(query, lang)
        query_vector = np.zeros((len(self.df), 1))
        for token in query:
            for i, term in enumerate(self.df):
                if token == term:
                    query_vector[i, 0] = 1
        return query_vector

    def similarity(self, doc_column, query_vector):
        sol = 0
        doc_column_norm = np.linalg.norm(doc_column)
        query_norm = np.linalg.norm(query_vector)
        for i in range(0,min(len(doc_column),len(query_vector))):
            sol += doc_column[i] * query_vector[i]
        div = doc_column_norm * query_norm if doc_column_norm != 0 and query_norm != 0 else 1
        return sol / div

    def get_ranking(self, query: str, first_n_results: int, offset: int = 0, lang: str = 'english') -> list[tuple[Document, float]]:
        self.generate_term_doc_matrix()
        U, S, Vt = self.U, self.S, self.Vt # this is now cached
        query_vector = self.generate_query_vector(query)
        query_vector = self._query_dimension_reduction(U, S, query_vector)

        ##
        score = 0
        doc_rank = []
        ##
        for i in range(len(Vt[0])):
            doc_column = Vt[:, i:i + 1]
            score = np.round(self.similarity(doc_column, query_vector), 4)
            # doc = self.documents[i]
            doc_rank.append((score[0], i))

        self.last_ranking = sorted(
            doc_rank, key=lambda rank_index: rank_index[0], reverse=True)
        return [(self.documents[doc], rank) for rank, doc in self.last_ranking[offset:offset + first_n_results]]
        