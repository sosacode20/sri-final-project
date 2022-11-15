from src import irs, document
from src.models import vector_space_model

irs_instance = irs.IRS()
doc1 = document.Document(1,
                         "Alicia in Wonderlans",
                         "Alicia was a Silly girl who run away from home to a fantasy world",
                         "english",
                         irs_instance)

doc2 = document.Document(2,
                         "simple shear flow past a flat plate in an incompressible fluid of small viscosity",
                         "in the study of high-speed viscous flow past a two-dimensional body it is usually necessary to consider a curved shock wave emitting from the nose or leading edge of the body .  consequently, there exists an inviscid rotational flow region between the shock wave and the boundary layer .  such a situation arises, for instance, in the study of the hypersonic viscous flow past a flat plate",
                         "english",
                         irs_instance)

vector_model = vector_space_model.Vector_Model(irs_instance, 0.6)
vector_model.add_document(doc1)
vector_model.add_document(doc2)

query = 'flow past'
ranking = vector_model.get_ranking(query)
print(ranking)
