from src import irs, document
from src.models import vector_space_model
from src.storage import Storage
from src import utils
from src.parser import CranParser
import time

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

def main():
    print(chr(27) + "[2J")
    print("Cargando la colección Cranfield de documentos...")
    start_time = time.time()

    storage = Storage()
    vector_model = vector_space_model.Vector_Model(utils.processing_text)
    cran = CranParser(utils.processing_text)
    irs_instance = irs.IRS(storage)
    irs_instance.add_model(vector_model)
    irs_instance.add_parser(cran)
    # irs_instance.add_document_collection("./data", "Cran", "Vector Space Model")

    print(chr(27) + "[2J")

    print("Colección cargada correctamente. Introduzca la consulta a realizar:\n")
    while(True):
        query = input()
        ranking = irs_instance.get_ranking(query, vector_model.get_model_name(), 5)
        for doc in ranking:
            print(f'DOC_ID:{doc[0]}\nDOC_NAME:{doc[1]}\n')
        end_time = time.time()
        print(time_convert(end_time - start_time))
        print("Introduzca 'q' para terminar la ejecución o cualquier otra tecla para realizar otra consulta:")
        if (input() == 'q'): break
    irs_instance.save()

if __name__ == "__main__":
    main()