from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
# stemming
from nltk.stem import PorterStemmer

class IRS:
    """This class has the propose of orchestrate the IRS process.
    """
    def __init__(self, path_to_index = './irs_data'):
        self.path_to_index = path_to_index

    def processing_text(self, raw_text:str, language:str) -> list[str]:
        """This method has the propose of processing the text
        Returns: a List of stemmed and normalized tokens
        """
        res = tokenize(raw_text, language)
        stop_list = stopwords.words(language)
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in res if token not in stop_list]
