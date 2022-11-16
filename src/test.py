import irs, document
from models import vector_space_model
from storage import Storage
import utils
from parser import CranParser

storage = Storage()

irs_instance = irs.IRS(storage)
doc1 = document.Document(1,
                         "Alicia in Wonderlans",
                         "Alicia was a Silly girl who run away from home to a fantasy world",
                         utils.processing_text,
                         "english")

doc2 = document.Document(2,
                         "simple shear flow past a flat plate in an incompressible fluid of small viscosity",
                         "in the study of high-speed viscous flow past a two-dimensional body it is usually necessary to consider a curved shock wave emitting from the nose or leading edge of the body .  consequently, there exists an inviscid rotational flow region between the shock wave and the boundary layer .  such a situation arises, for instance, in the study of the hypersonic viscous flow past a flat plate",
                         utils.processing_text,
                         "english")

vector_model = vector_space_model.Vector_Model(utils.processing_text)
vector_model.add_document(doc1)
vector_model.add_document(doc2)
# pera que eso lo cambio yo
# tengo que agregar un metodo rapidito a IRS para agregar documentos independientes
cran = CranParser(utils.processing_text)
irs_instance.add_model(vector_model)
# irs_instance.add_parser(cran)
# irs_instance.add_document_collection("./data", "Cran", "Vector Space Model")

query = 'flow past'
ranking = vector_model.get_ranking(query, 5)
print([doc.doc_name for doc in ranking])
