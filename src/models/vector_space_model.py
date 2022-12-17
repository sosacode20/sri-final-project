from src.model import Model
from typing import Callable
from src.document import Document
import numpy as np
import math


class Vector_Model(Model):

    def __init__(self, text_processor: Callable[[str, str], list[str]]):
        super().__init__(text_processor)
        """
        This is the set of all words in the collection of documents
        """
        self.tf: dict[tuple[str, int], float] = {}
        """
        This is the relative frequency of a token in a document. 
        Dictionary where the key is a tuple (term_str, doc_index) and the value is the tf of the term in the document"""
        self.df: dict[str, int] = {}
        """
        This is the amount of documents in which the term is present
        """
        self.smooth_constant: float = 0.5
        """
        This is the smooth constant for the query formula
        """
        self.document_vector_dirty = False
        """
        This is a property to know when is necessary to recalculate the document vectors
        """
        self.document_vectors: list[list[tuple[str, float]]] = []
        """
        This is the dictionary where the key is the document_id and the value is a list of tuples (term_index, tf * idf)
        """
        # This acts as a cache for storing the last ranking of a consult, this is in the case of handling result pages
        self.last_ranking: list[tuple[float, int]] = []

    def get_name(self):
        return "Vector Space Model"

    def set_smooth_constant(self, smooth: float):
        """This method is for setting the smooth constant for the query formula

        Args:
            smooth (float): Smooth Constant
        """
        self.smooth_constant = max(0.1, min(1, smooth))

    def add_document(self, document: Document):
        # tell the model that needs to recalculate the vectors of documents
        self.document_vector_dirty = True
        self.documents.append(document)
        title = document.doc_normalized_name
        body = document.doc_normalized_body
        text = title + body
        term_frequency = self.__get_tf(text)
        # Add the document to the list of documents
        # Update the amount of documents in which the term is
        for token in term_frequency:
            if token in self.df:
                self.df[token] += 1
            else:
                self.df[token] = 1
            self.tf[(token, len(self.documents) - 1)] = term_frequency[token]

    def __get_tf(self, text: list[str]) -> dict[str, float]:
        """Generate the normalized term frequency of a text as a dictionary

        Args:
            text (list[str]): A list of normalized string tokens

        Returns:
            dict[str, int]: Dictionary where the key is a term and the value is the frequency of the term in the text
        """
        tf: dict[str, float] = { }# Dictionary where the key is a term and the value is the frequency of the term in the document
        
        max_frequency = 0  # The maximum frequency of a term in the document
        for token in text:
            if token in tf:
                tf[token] += 1
            else:
                tf[token] = 1
            if tf[token] > max_frequency:
                max_frequency = tf[token]
        # Normalize the term frequency
        for token in tf:
            tf[token] = tf[token] / max_frequency
        return tf

    def generate_document_vectors(self):
        """Generate the document vectors for the model
        Returns:
            None: The documents vector are calculated here and stored in the model for later use
        """
        if not self.document_vector_dirty:  # If the vectors are already calculated there is no need for recalculation
            return

        self.document_vector_dirty = False
        self.document_vectors = []

        for doc_index, doc in enumerate(self.documents):
            self.document_vectors.append([])
            for term in (doc.doc_normalized_name + doc.doc_normalized_body):
                idf: float = math.log(len(self.documents) /
                             self.df[term])
                tf: float = 0
                if (term, doc_index) in self.tf:
                    tf = self.tf[(term, doc_index)]
                    self.document_vectors[doc_index].append(
                        (term, tf * idf))

    def generate_query_vector(self, query: str, lang: str = 'english'):
        """Return the query vector given a string query and a language for the stemming process

        Args:
            query (str): This is the text of the query. In this method it's normalized
            lang (str, optional): The language of the query. Required for the query text processing. Defaults to 'english'.

        Returns:
            NDArray[float64]: A numpy array representing the query vector
        """
        tokenized_query = self.text_processor(query, lang)
        tf = self.__get_tf(tokenized_query)
        # for each term in vocabulary calculate its tf in the query
        a = self.smooth_constant

        query_vector: list[tuple[str, float]] = []
        for term in tokenized_query:
            if term in self.df:  # if the term of the query is in the vocabulary
                document_length = len(self.documents)
                term_document_frequency = self.df[term]
                # query_vector.append((term_index,a + (1 + a) * tf[vocabulary[term_index]]) * np.log(document_length / term_document_frequency))
                query_vector.append((term, (a + (1 - a) * tf[term]) * math.log(
                    document_length / term_document_frequency)))
        return query_vector

    # [ ]: se escribe similarity
    def similitud(self, vector1: list[tuple[str, float]], vector2: list[tuple[str, float]]) -> float:
        """Calculate the similitud between two vectors

        Args:
            vector1 (list[tuple[int,float]]): A list of tuples (term_index, tf * idf)
            vector2 (list[tuple[int,float]]): A list of tuples (term_index, tf * idf)

        Returns:
            float: The similitud between the two vectors
        """
        dot_product = 0
        for i in range(len(vector1)):
            for j in range(len(vector2)):
                if vector1[i][0] == vector2[j][0]:
                    dot_product += vector1[i][1] * vector2[j][1]
                    break
        norm = math.sqrt(sum([vector1[i][1] ** 2 for i in range(len(vector1))])
                         ) * sum([vector2[i][1] ** 2 for i in range(len(vector2))])
        if norm == 0:
            return 0
        return dot_product / norm

    def get_ranking(self, query: str, first_n_results: int, lang: str = 'english'):
        self.generate_document_vectors()
        query_vector = self.generate_query_vector(query, lang)
        doc_rank: list[tuple[float, int]] = []
        for index, _ in enumerate(self.documents):
            doc_vector = self.document_vectors[index]
            sim = self.similitud(doc_vector, query_vector)
            doc_rank.append((sim, index))
        self.last_ranking = sorted(
            doc_rank, key=lambda rank_index: rank_index[0], reverse=True)
        return [(self.get_document_by_id(doc), rank) for rank, doc in self.last_ranking[:first_n_results]]
        return [self.documents[x[1]] for x in self.last_ranking[:first_n_results]]
