from src.model import Model
from typing import Callable
# from ..document import Document
from src.document import Document
import numpy as np
import math

class Probabilistic_Model(Model):

    def __init__(self, text_processor: Callable[[str, str], list[str]]):
        super().__init__(text_processor)
        self.inverted_index = {}
        self.weights = {}
        self.ranked = []
        self.dirty = 0

    def get_name(self):
        return "Probabilistic_Model"

    def document_frequency(self, term: str) -> int:
        return len(self.inverted_index[term])

    def inverse_document_frequency(self, term: str, df: int) -> float:
        aux = len(self.documents) / df

        return math.log(aux)
    #[ ]
    def add_document(self, document: Document):
        self.dirty = 1
        self.documents.append(document)

    def generate_inverted_index(self):
        self.inverted_index = {}
        for i in range(len(self.documents)):
            for term in self.documents[i].doc_normalized_name + self.documents[i].doc_normalized_body:
                if term not in self.inverted_index:
                    self.inverted_index[term] = set()
                self.inverted_index[term].add(i)

    def rsv_weight(self) -> None:
        N = len(self.documents)
        self.weights = { }
        for term in self.inverted_index:
            p = self.document_frequency(term) / (N + 0.5)
            t1 = self.inverse_document_frequency(term, p)
            t2 = p/(1-p)
            self.weights[term] = t1 + math.log(t2)

    #[ ]
    def rsv_doc_query(self, query:str, doc_id:int, query_vector:list[str]):
        score = 0
        if doc_id >= len(self.documents):
            pass
        doc = self.documents[doc_id]

        for term in query_vector:
            if term in doc.doc_normalized_name + doc.doc_normalized_body:
                score += self.weights[term]
        return score

    #[ ]
    def _get_ranking(self, query:str, query_vector: list[str]):
        docs = set()
        for term in query_vector:
            if term in self.inverted_index:
                docs_with_term = self.inverted_index[term]
                for docs_id in docs_with_term:
                    docs.add(docs_id)

        scores = []
        for doc in docs:
            scores.append((doc, self.rsv_doc_query(query, doc, query_vector)))

        self.ranked = sorted(scores, key=lambda x: x[1], reverse=True)
        return self.ranked

    def get_ranking(self, query:str, amount:int, offset:int, lang:str = 'english') -> list[tuple[Document, int]]:
        if self.dirty:
            self.generate_inverted_index()
            self.rsv_weight()
            self.dirty = 0
        query_vector = self.generate_query_vector(query, lang)
        ranking = self._get_ranking(query, query_vector)

        ## pseudo-feedback
        i = 0
        new_ranking = []
        while (i < 10) and ranking != new_ranking:
            self.recompute_weights(query_vector)
            new_ranking = self._get_ranking(query, query_vector)
            i += 1
        ranking = new_ranking

        return [(self.documents[doc], rank) for doc, rank in ranking[offset: offset + amount]]

    def generate_query_vector(self, query: set, lang: str = 'english'):
        return self.text_processor(query, lang)
 
    #[ ]
    def recompute_weights(self, query_vector: list[str]):
        relevant_docs = []
        for idx in range(5):
            doc_id = self.ranked[idx][0]
            relevant_docs.append(self.documents[doc_id])
        
        N = len(self.documents)
        ni = len(relevant_docs)

        for term in query_vector:
            if term in self.weights.keys():
                Vi = 0
                for doc in relevant_docs:
                    if term in doc.doc_normalized_name + doc.doc_normalized_body:
                        Vi += 1
                p = (Vi + 0.5) / (ni + 1)
                u = (self.document_frequency(term) - Vi + 0.5) / (N - ni + 1)
                self.weights[term] = math.log((1-u)/u) + math.log(p/(1-p))