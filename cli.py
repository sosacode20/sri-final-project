from src import irs, document
from src.models import vector_space_model
from src.storage import Storage
from src import utils
from src.parser import CranParser

def main():
    print(chr(27) + "[2J")
    print("Cargando la colección Cranfield de documentos...")

    storage = Storage()
    vector_model = vector_space_model.Vector_Model(utils.processing_text)
    cran = CranParser(utils.processing_text)
    irs_instance = irs.IRS(storage)
    irs_instance.add_model(vector_model)
    irs_instance.add_parser(cran)
    irs_instance.add_document_collection("./data", "Cran", "Vector Space Model")

    print(chr(27) + "[2J")

    print("Colección cargada correctamente. Introduzca la consulta a realizar:\n")
    while(True):
        query = input()
        ranking = vector_model.get_ranking(query, 5)
        for doc in ranking:
            print(f'DOC_ID:{doc.doc_id}\nDOC_NAME:{doc.doc_name}\n')
        print("Introduzca 'q' para terminar la ejecución o cualquier otra tecla para realizar otra consulta:")
        if (input() == 'q'): break

if __name__ == "__main__":
    main()