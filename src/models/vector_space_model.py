# from ..model import Model
from ..model import Model
from ..irs import IRS
# from ..document import Document
from document import Document
import numpy as np


class Vector_Model(Model):

    def __init__(self, irs: IRS, smooth_constant: float):
        super().__init__(irs)
        self.documents: dict[int, Document] = {}
        # TODO: Store this in a binary tree to remove ordering... for now it is an ordered list
        self.vocabulary = []
        # Dictionary where the key is a tuple (term_str, doc_index) and the value is the tf of the term in the document
        self.tf: dict[tuple[str, int], float] = {}
        # Dictionary where the key is a term and the value is the frequency of the term in the collection of documents
        self.tdf: dict[str, int] = {}
        self.smooth_constant = smooth_constant
        # Dictionary where the key is an int and the value is a ndarray of floats
        # TODO: Change the annotation for the type of the value to an ndarray of floats
        # self.tf_idf : dict[int, np.ndarray] = {}
        # TODO: Refactor this in a way that is a dirty property for knowing when to recalculate the vectors
        self.__document_vectors = np.zeros((1,))
        self.__document_vector_dirty = True
        self.last_ranking: list[tuple[float, int]] = [] # This acts as a cache for storing the last ranking of a consult, this is in the case of handling result pages

    def get_model_name(self):
        return "Vector Space Model"

    def add_document(self, document: Document):
        # Process all word tokens of the document
        id = document.get_doc_id()
        if id in self.documents:
            raise Exception(
                "The document is already in the collection of documents")
        # tell the model that need to recalculate the vectors of documents
        self.__document_vector_dirty = True
        self.documents[id] = document
        title = document.doc_normalized_name
        body = document.doc_normalized_body
        text = title + body
        term_frequency = self.__get_tf(text)
        # Add the document to the list of documents
        # Update the amount of documents in which the term is
        for token in term_frequency:
            if token in self.tdf:
                self.tdf[token] += 1
            else:
                self.tdf[token] = 1
            self.tf[(token, id)] = term_frequency[token]
        # TODO: update the weights in each document vector

    def __get_tf(self, text: list[str]) -> dict[str, float]:
        """Generate the normalized term frequency of a text as a dictionary

        Args:
            text (list[str]): A list of normalized string tokens

        Returns:
            dict[str, int]: Dictionary where the key is a term and the value is the frequency of the term in the text
        """
        tf: dict[str, float] = {
        }  # Dictionary where the key is a term and the value is the frequency of the term in the document
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
        if not self.__document_vector_dirty:  # If the vectors are already calculated there is no need for recalculation
            return
        self.__document_vector_dirty = False
        # Create the vocabulary sorted
        self.vocabulary = sorted(self.tdf.keys())
        self.__document_vectors = np.zeros(
            (len(self.documents), len(self.vocabulary)))
        for doc_index in range(len(self.documents)):
            for term_index in range(len(self.vocabulary)):
                # term = self.vocabulary[j]
                idf = np.log(len(self.documents) /
                             self.tdf[self.vocabulary[term_index]])
                tf = self.tf[(self.vocabulary[term_index], doc_index)]
                self.__document_vectors[doc_index, term_index] = tf * idf

    def generate_query_vector(self, query: str, lang: str = 'english'):
        """Return the query vector given a string query and a language for the stemming process

        Args:
            query (str): This is the text of the query. In this method it's normalized
            lang (str, optional): The language of the query. Required for the query text processing. Defaults to 'english'.

        Returns:
            NDArray[float64]: A numpy array representing the query vector
        """
        tokenized_query = self.irs.processing_text(query, lang)
        tf = self.__get_tf(tokenized_query)
        vocabulary = self.vocabulary  # must be sorted
        # for each term in vocabulary calculate its tf in the query
        a = self.smooth_constant
        query_vector = np.zeros((len(vocabulary),))
        for term_index in range(len(vocabulary)):
            if vocabulary[term_index] in tf:
                document_length = len(self.documents)
                term_document_frequency = self.tdf[vocabulary[term_index]]
                query_vector[term_index] = (
                    a + (1 + a) * tf[vocabulary[term_index]]) * np.log(document_length / term_document_frequency)
            else:
                query_vector[term_index] = 0
        return query_vector

    def similitud(self, vector1: np.ndarray, vector2: np.ndarray):
        # numpy dot product
        return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    def get_ranking(self, query: str, lang: str = 'english'):
        self.generate_document_vectors()
        query_vector = self.generate_query_vector(query, lang)
        doc_rank: list[tuple[float, int]] = []
        for i in range(len(self.documents)):
            doc_vector = self.__document_vectors[i]
            sim = self.similitud(doc_vector, query_vector)
            doc_rank.append((sim, i))
        self.last_ranking = sorted(doc_rank, key = lambda x : x[0])
        return self.last_ranking

