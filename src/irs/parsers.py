class parse:

    def __init__(self, format_list = None):
        self.formats = format_list

    def parse(self, file):
        pass

class cran_parser(parse):

    def __init__(self, ):
        super().__init__([".1400"])
        self.corpus = "cran"

    def parse(self, file):
        docs = []
        doc_id = ''
        text = ''
        subject = ''
        in_subject = 0
        in_text = 0
        while True:
            line = file.readline()
            if len(line.split())>0:
                if line.split()[0]=='.I':
                    if in_text:
                        docs.append([subject, text, doc_id])
                        in_text=0
                        subject=''
                        text=''
                        doc_id=''
                    doc_id = line.split()[1]
                elif line.split()[0]=='.A':
                    in_subject = 0
                    line = file.readline()
                    text+=line
                elif line.split()[0]=='.B':
                    line = file.readline()
                    text+=line
                elif line.split()[0]=='.W':
                    in_text = 1
                elif in_text:
                    text+=line
                elif line.split()[0]=='.T':
                    in_subject = 1
                elif in_subject:
                    subject+=line
            elif not line:
                docs.append([subject, text, doc_id])
                break
            
        return docs
