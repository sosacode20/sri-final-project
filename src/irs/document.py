class document:
    def __init__(self, doc_id, doc_name, doc_body, doc_lang, irs):
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.doc_body = doc_body
        self.doc_lang = doc_lang
        self.irs = irs
        self.doc_normalized_name = irs.processing_text(doc_name, doc_lang)
        self.doc_normalized_body = irs.processing_text(doc_body, doc_lang)

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
        return "doc_id: " + self.doc_id + ""