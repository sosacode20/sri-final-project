# The purpose of this file is for quick testing. This is not part of the solution

import irs, document
from models import vector_space_model
from storage import Storage
import utils
from irs_parser import CranParser

storage = Storage()

irs_instance = irs.IRS(storage)

vector_model = vector_space_model.Vector_Model(utils.processing_text)

cran = CranParser(utils.processing_text)
irs_instance.add_model(vector_model)
irs_instance.add_parser(cran)
# irs_instance.add_document_collection("./data", "Cran", "Vector Space Model")

queries = ['transition studies and skin friction measurements', 'combined effects', 'boundary layer']

for query in queries:
    print(f'\n\nThe query was: {query}\n\n---------------------------------------------------\n')
    ranking = irs_instance.get_ranking(query, vector_model.get_name(), 10)
    for rank in ranking:
        print(f'\n{rank}\n')

irs_instance.save()

