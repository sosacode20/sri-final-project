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
    # Uncomment the next line if the .pkl file is deleted and having the collection in the file './data'
    # irs_instance.add_document_collection("./data", cran.get_pretty_name(), vector_model.get_model_name())
    
    finish_loading_documents = time.time()
    print(chr(27) + "[2J")
    print(f'La colección de documentos se cargó en {finish_loading_documents - start_time} segundos')

    print("Colección cargada correctamente.\n")
    while(True):
        query = input('Introduzca la consulta a realizar o escriba \'q\' para salir: ')
        # if query without whitespace is q then break
        query = query.strip()
        match query:
            case 'q':
                break
            case '':
                print("La consulta no puede estar vacía.")
                continue
            case _:
                print("Procesando consulta...\n")
                print('-----------------------------------------------------')
                print('-----------------------------------------------------\n')
        start_time = time.time()
        ranking = irs_instance.get_ranking(query, vector_model.get_model_name(), 5)
        for doc in ranking:
            print(f'Document ID: {doc[0]}\nDocument Name: {doc[1]}\n')
        end_time = time.time()
        print('The ranking took {0} seconds to be generated\n\n'.format(end_time - start_time))
        print('-----------------------------------------------------')
        print('-----------------------------------------------------\n')

    irs_instance.save()

if __name__ == "__main__":
    main()