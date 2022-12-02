import re
from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
import string
# stemming
from nltk.stem import PorterStemmer
import os


def processing_text(raw_text: str, language: str) -> list[str]:
    """This method has the propose of processing the text
    Returns: a List of stemmed and normalized tokens
    """
    # raw_text = re.sub(r'[^\w\s]', '', raw_text)
    res = tokenize(raw_text, language)
    stop_list = stopwords.words(language) + [*string.punctuation]
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in res if (token not in stop_list) and len(token) >= 3]


def get_all_files_with_extension(path: str, extensions: list[str]) -> list[str]:
    """This method returns the absolute path off all the files with an extension

    Args:
        path (str): The path from where to start the search of files
        extensions (list[str]): The list of extensions. Must end in for example: '.ext' not 'ext'

    Returns:
        list[str]: A list containing the absolute path of all the files with the given extensions
    """
    file_paths: list[str] = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(extensions[0]):
                file_paths.append(os.path.join(root, file))
    return file_paths
