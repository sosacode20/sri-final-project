from typing import Callable

class Document:
    """This is a Document object containing the original Document and the normalized version of it.
    """
    def __init__(self, doc_id: int, doc_name: str, doc_body: str, text_processor: Callable[[str,str],list[str]], doc_lang: str):
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.doc_body = doc_body
        self.doc_lang = doc_lang
        self.text_processor = text_processor
        self.doc_normalized_name = text_processor(doc_name, doc_lang)
        self.doc_normalized_body = text_processor(doc_body, doc_lang)

    def get_doc_id(self):
        return self.doc_id

    def get_doc_name(self):
        return self.doc_name

    def get_doc_content(self):
        return self.doc_content

    def set_doc_id(self, doc_id):
        self.doc_id = doc_id

    def set_doc_name(self, doc_name):
        self.doc_name = doc_name

    def set_doc_content(self, doc_content):
        self.doc_content = doc_content

    def __str__(self):
        return f'doc_id: {self.doc_id}, doc_title: {self.doc_name}'
