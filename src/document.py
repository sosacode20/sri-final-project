# Represents a general document
# A document always has a title and a body
# But in general it can be model as a tree of nodes
# Each node has a (type,value) and a list of children
import xml.dom.minidom as minidom

class Node:
    """This class is a node in a document tree
    A node has a type and a value
    """
    def __init__(self, key, value):
        self.type = type
        self.value = value
        self.children = []

    def __repr__(self):
        return "Node(%s,%s)" % (self.type, self.value)

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.children)

    def __getitem__(self, i):
        return self.children[i]

    def __setitem__(self, i, node):
        self.children[i] = node

    def __delitem__(self, i):
        del self.children[i]

    def __iter__(self):
        return self.children.__iter__()

    def append(self, node):
        self.children.append(node)

    def extend(self, nodes):
        self.children.extend(nodes)

    def insert(self, i, node):
        self.children.insert(i, node)

    def remove(self, node):
        self.children.remove(node)

    def index(self, node):
        return self.children.index(node)

    def count(self, node):
        return self.children.count(node)

    def pop(self, i=-1):
        return self.children.pop(i)

    def toxml(self, doc):
        """Converts a node to XML
        """
        node = doc.createElement(self.type)
        if self.value:
            node.appendChild(doc.createTextNode(self.value))
        for child in self.children:
            node.appendChild(child.toxml(doc))
        return node
    


class Document:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body
        self.nodes = []

    
        