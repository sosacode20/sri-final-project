
class Document:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body
        self.nodes = []
        