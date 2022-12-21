from src.irs import IRS
from src.models import vector_space_model, probabilistic_model
from src.model import Model
from src.storage import Storage
from src import utils
from src.irs_parser import CranParser, ReutersParser, Parser

test_queries_dir = "./data/queries/"

def main():
    storage = Storage()
    irs_instance = IRS(storage)
    vector_model = vector_space_model.VectorSpaceModel(utils.processing_text)
    prob_model = probabilistic_model.ProbabilisticModel(utils.processing_text)
    
    cran_parser = CranParser(utils.processing_text)
    reuters_parser = ReutersParser(utils.processing_text)

    irs_instance.add_model(vector_model)
    irs_instance.add_parser(cran_parser)
    irs_instance.add_document_collection("./data", "cran", vector_model.get_name())

    cran_test_queries = 

if __name__ == "__main__":
    main()