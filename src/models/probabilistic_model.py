from src.model import Model
from typing import Callable
# from ..document import Document
from src.document import Document
import numpy as np
import math

class Probabilistic_Model(Model):

    def __init__(self, text_processor: Callable[[str, str], list[str]]):
        super().__init__(text_processor)

        self.document_vectors: list[list[str]] = []
        """
        This is the dictionary where the key is the document_id and the value is a list of tuples (term_index, occurrence)
        """
        # This acts as a cache for storing the last ranking of a consult, this is in the case of handling result pages
        self.last_ranking: list[tuple[float, int]] = []
        
        self.query_document_relevance: dict[tuple[str, int], dict[str, float]] = {}

        self.query_document_not_relevance: dict[tuple[str, int], dict[str, float]] = {}
        """
        This contains the relevance of a query in a document
        """

    def get_name(self):
        return "Probabilistic_Model"

    def add_document(self, document: Document):
        self.documents.append(document)
        self.document_vectors.append([])
        for term in (document.doc_normalized_name + document.doc_normalized_body):
            self.document_vectors[-1].append(term)

    def generate_document_vectors(self):
        """Generate the document vectors for the model
        Returns:
            None: The documents vector are calculated here and stored in the model for later use
        """
        self.document_vectors = []

        for doc_index, doc in enumerate(self.documents):
            self.document_vectors.append([])
            for term in (doc.doc_normalized_name + doc.doc_normalized_body):
                self.document_vectors[doc_index].append(term)

    def get_term_frequency(self, term: str) -> float:
        n_i = 0
        for doc in (self.document_vectors):
            if term in doc:
                n_i += 1
        return n_i / len(self.documents)

    def generate_query_vector(self, query: set, lang: str = 'english'):
        return self.text_processor(query, lang)

    def get_relevance(self, query, document_id, term) -> float:
        if (query, document_id) in self.query_document_relevance:
            if term in self.query_document_relevance[(query, document_id)]:
                dr = self.query_document_relevance[(query, document_id)][term]
                dnr = self.query_document_not_relevance[(query, document_id)][term]
                return (dr, dnr) 

            dr = 0.5
            dnr = self.get_term_frequency(term)
            self.query_document_relevance[(query, document_id)][term] = dr
            self.query_document_not_relevance[(query, document_id)][term] = dnr
            return (dr, dnr)

        dr = 0.5
        dnr = self.get_term_frequency(term)

        self.query_document_relevance[(query, document_id)] = { term:dr }
        self.query_document_not_relevance[(query, document_id)] = { term:dnr }

        return (dr, dnr)

    def similarity(self, raw_query:str, query: list[str], document: list[str], document_id: int) -> float:
        """Calculate the similarity between a query and a document"""
        similarity = 0

        for common_term in query:
            if common_term in document:
                p_i, r_i = self.get_relevance(raw_query, document_id, common_term)
                similarity += math.log((p_i * (1 - r_i)) / (r_i * (1 - p_i)))

        return (0 if similarity == 0 else math.log(similarity))
            
    def get_ranking(self, query: str, first_n_results: int, offset:int, lang: str = 'english') -> list[tuple[Document, int]]:
        query_vector = self.generate_query_vector(query, lang)
        doc_rank: list[tuple[float, int]] = []
        for index, _ in enumerate(self.documents):
            doc_vector = self.document_vectors[index]
            sim = self.similarity(query, query_vector, doc_vector, index)
            doc_rank.append((sim, index))
        self.last_ranking = sorted(
            doc_rank, key=lambda rank_index: rank_index[0], reverse=True)
        
        #the commented one only returns ranking != 0
        # return [] if self.lastranking[0][0] == 0 else [(self.documents[doc], rank) for rank, doc in self.last_ranking[offset: offset + first_n_results]]
        return [(self.documents[doc], rank) for rank, doc in self.last_ranking[offset: offset + first_n_results]]

    def total_relevant_documents(self) -> int:
        total = 0
        i = 0
        while(self.last_ranking[i][0] != 0):
            total += 1
            i += 1
        return total

    def total_ocurrences(self, term: str) -> int:
        total = 0
        for doc in self.document_vectors:
            if term in doc:
                total += 1
        return total

    #[ ]: limit tiene que ser menot que relevant_documents_cant
    def pseudo_feedback(self, raw_query:str, lang:str = 'english', limit:int = 10):
        query_vector = self.generate_query_vector(raw_query, lang)
        V = self.total_relevant_documents()
        N = len(self.documents)

        ### Calculating term ocurrences in relevant documents
        for term in query_vector:
            ni = self.total_ocurrences(term)
            Vi = 0
            doc_index_list = []
            for i in range(limit):
                rank, doc_index = self.last_ranking[i]
                if rank == 0:
                    break
                if term in self.document_vectors[doc_index]:
                    Vi += 1
                    doc_index_list.append(doc_index)
            for doc_index in doc_index_list:
                self.query_document_relevance[(raw_query, doc_index)][term] = (Vi / V)
                self.query_document_not_relevance[(raw_query, doc_index)][term] = (ni - Vi) / (N - V)
                