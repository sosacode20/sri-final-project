from src.document import Document
from typing import Callable
from io import TextIOWrapper


class Parser:
    def __init__(
        self, text_processor: Callable[[str, str], list[str]], lang: str = "english"
    ):
        self.text_processor = text_processor
        self.lang = lang

    def get_pretty_name(self) -> str:
        """Returns the pretty name of this parser

        Returns:
            str: The name of the parser
        """
        return self.__class__.__name__

    def get_extension_list(self) -> list[str]:
        """Returns the list of the formats this parser handles
        Returns:
            list[str]: A list with all the formats. Each element has the form 'ext' not '.ext',
        """
        return [".txt"]

    def parse(self, file: TextIOWrapper):
        """This method receives a file and parse it's contents returning a list of documents

        Args:
            file (_type_): _description_
        Returns:
            list[Document]: A list with the normalized documents
        """
        return [Document(0, "empty", "empty", self.text_processor, self.lang)]


class CranParser(Parser):
    def __init__(
        self, text_processor: Callable[[str, str], list[str]], lang: str = "english"
    ):
        super().__init__(text_processor, lang)

    def get_pretty_name(self) -> str:
        return "Cran"

    def get_extension_list(self):
        return ["all.1400"]

    #FIXME: Errors while files are not well formatted
    def parse(self, file: TextIOWrapper) -> list[Document]:
        docs = []
        doc_id = 0
        text = ""
        subject = ""
        in_subject = 0
        in_text = 0
        while True:
            line = file.readline()
            if len(line.split()) > 0:
                if line.split()[0] == ".I":
                    if in_text:
                        doc = Document(
                            doc_id, subject, text, self.text_processor, self.lang
                        )
                        docs.append(doc)
                        in_text = 0
                        subject = ""
                        text = ""
                    doc_id = int(line.split()[1])
                elif line.split()[0] == ".A":
                    in_subject = 0
                    line = file.readline()
                    text += line
                elif line.split()[0] == ".B":
                    line = file.readline()
                    text += line
                elif line.split()[0] == ".W":
                    in_text = 1
                elif in_text:
                    text += line
                elif line.split()[0] == ".T":
                    in_subject = 1
                elif in_subject:
                    subject += line
            elif not line:
                doc = Document(doc_id, subject, text, self.text_processor, self.lang)
                docs.append(doc)
                break

        return docs

class NewsGroupParser(Parser):

        # def _get_document(self, file):
        #     text = ''
        #     subject = ''
        #     s = 1
        #     while True:
        #         line = file.readline()
        #         if not line:
        #             break
        #         text += line
        #         if s and line.split()[0] == 'Subject:':
        #             s = 0
        #             subject = ' '.join(line.split()[1:])
        #     return [subject, text]
    #Hasta aqui es la implementacion de aldair 

    def __init__(
        self, text_processor: Callable[[str, str], list[str]], lang: str = "english"
    ):
        super().__init__(text_processor, lang)

    def get_pretty_name(self) -> str:
        return "NewsGroup"

    def get_extension_list(self):
        return [""]

    def parse(self, file: TextIOWrapper) -> list[Document]:
        docs = []
        doc_id = 0
        text = ""
        title = ""
        in_text = 0
        while True:
            line = file.readline()
            if len(line) > 0:
                if line.find("<REUTERS") != -1:
                    doc_id = int(line.split("NEWID=")[1].split('"')[1])
                elif line.find("<TITLE>") != -1:
                    title = line.split("<TITLE>")[1].split("</TITLE>")[0]
                elif line.find("<BODY>") != -1:
                    in_text = 1
                    text += line.split("<BODY>")[1]
                elif line.find("</BODY>") != -1:
                    in_text = 0
                    doc = Document(
                        doc_id, title, text, self.text_processor, self.lang
                    )
                    docs.append(doc)
                    text = ""
                    title = ""
                elif in_text:
                    text += line
            elif not line:
                break
        return docs

class ReutersParser(Parser):
    def __init__(
        self, text_processor: Callable[[str, str], list[str]], lang: str = "english"
    ):
        super().__init__(text_processor, lang)

    def get_pretty_name(self) -> str:
        return "Reuters"

    def get_extension_list(self):
        return [".sgm"]

    def parse(self, file: TextIOWrapper) -> list[Document]:
        docs = []
        doc_id = 0
        text = ""
        title = ""
        in_text = 0
        while True:
            line = file.readline()
            if len(line) > 0:
                if line.find("<REUTERS") != -1:
                    doc_id = int(line.split("NEWID=")[1].split('"')[1])
                elif line.find("<TITLE>") != -1:
                    title = line.split("<TITLE>")[1].split("</TITLE>")[0]
                elif line.find("<BODY>") != -1:
                    in_text = 1
                    text += line.split("<BODY>")[1]
                elif line.find("</BODY>") != -1:
                    in_text = 0
                    doc = Document(
                        doc_id, title, text, self.text_processor, self.lang
                    )
                    docs.append(doc)
                    text = ""
                    title = ""
                elif in_text:
                    text += line
            elif not line:
                break
        return docs