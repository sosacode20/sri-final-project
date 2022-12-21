from src import irs, document
from src.models import vector_space_model, probabilistic_model, lsi_model
from src.storage import Storage
from src import utils
from src.irs_parser import CranParser, ReutersParser
import time
import math

#define evaluation metrics


#parse files cran.qry and cranqrel in /data/queries/cran
def parse_cran_queries():
    queries = []
    with open("./data/queries/cran/cran.qry", "r") as f:
        for line in f:
            if line.startswith(".I"):
                query = {}
                query["id"] = line.split(" ")[1].strip("\n")
            elif line.startswith(".W"):
                query["text"] = ""
            else:
                query["text"] += line
            if line.startswith(".I"):
                queries.append(query)
    return queries

def parse_cran_qrels():
    qrels = {}
    with open("./data/queries/cran/cranqrel", "r") as f:
        for line in f:
            line = line.split(" ")
            if line[0] not in qrels:
                qrels[line[0]] = []
            qrels[line[0]].append(int(line[1]))
    return qrels

def main():
    #initialize the three models
    storage = Storage()
    vector = vector_space_model.Vector_Model(utils.processing_text)
    prob = probabilistic_model.Probabilistic_Model(utils.processing_text)
    lsi = lsi_model.LSI_Model(utils.processing_text)

    parser = CranParser(utils.processing_text)

    irs_vector = irs.IRS(storage)
    irs_prob = irs.IRS(storage)
    irs_lsi = irs.IRS(storage)

    irs_vector.add_parser(parser)
    irs_prob.add_parser(parser)
    irs_lsi.add_parser(parser)

    irs_vector.add_model(vector)
    irs_prob.add_model(prob)
    irs_lsi.add_model(lsi)

    irs_vector.add_document_collection("./data", parser.get_pretty_name(), vector.get_name())
    irs_prob.add_document_collection("./data", parser.get_pretty_name(), prob.get_name())
    irs_lsi.add_document_collection("./data", parser.get_pretty_name(), lsi.get_name())

    queries = parse_cran_queries()
    rels = parse_cran_qrels()

    #feed the queries into the models
    query = queries[0]
    query_results_vector = irs_vector.get_ranking(query["text"], vector.get_name(), len(irs_vector.models["Vector Space Model"].documents), 0)[0]
    query_results_prob = irs_prob.get_ranking(query["text"], prob.get_name(), len(irs_prob.models["Probabilistic_Model"].documents), 0)[0]
    query_results_lsi = irs_lsi.get_ranking(query["text"], lsi.get_name(), len(irs_lsi.models["LSI_Model"].documents), 0)[0]

    #calculate the evaluation metrics
    #precision
    precision_vector = 0
    precision_prob = 0
    precision_lsi = 0
    for i in range(100):
        if query_results_vector[i][0] in rels[str(int(query["id"]))]:
            precision_vector += 1
        if query_results_prob[i][0] in rels[str(int(query["id"]))]:
            precision_prob += 1
        if query_results_lsi[i][0] in rels[str(int(query["id"]))]:
            precision_lsi += 1
    precision_vector = precision_vector / 10
    precision_prob = precision_prob / 10
    precision_lsi = precision_lsi / 10

    #recall
    recall_vector = 0
    recall_prob = 0
    recall_lsi = 0
    for i in range(100):
        if query_results_vector[i][0] in rels[str(int(query["id"]))]:
            recall_vector += 1
        if query_results_prob[i][0] in rels[str(int(query["id"]))]:
            recall_prob += 1
        if query_results_lsi[i][0] in rels[str(int(query["id"]))]:
            recall_lsi += 1
    recall_vector = recall_vector / len(rels[str(int(query["id"]))])
    recall_prob = recall_prob / len(rels[str(int(query["id"]))])
    recall_lsi = recall_lsi / len(rels[str(int(query["id"]))])

    #F1
    f1_vector = 2 * (precision_vector * recall_vector) / (precision_vector + recall_vector)
    f1_prob = 2 * (precision_prob * recall_prob) / (precision_prob + recall_prob)
    f1_lsi = 2 * (precision_lsi * recall_lsi) / (precision_lsi + recall_lsi)

    return
    
#compare the results with the cranqrel file


if __name__ == "__main__":
    main()








#for guidance
        # model = self.models[model_name]
        # all_files = get_all_files_with_extension(path, parser.get_extension_list())
        # for file_path in all_files:
        #     with open(file_path, 'r') as file:
        #         documents = parser.parse(file)
        #         for document in documents:
        #             model.add_document(document)