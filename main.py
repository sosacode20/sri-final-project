#IRS modules
from src.irs import IRS
from src.models import vector_space_model, probabilistic_model, lsi_model
from src.model import Model
from src.storage import Storage
from src import utils
from src.irs_parser import CranParser, ReutersParser, Parser
from fastapi.testclient import TestClient

#Web application modules
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

#For testing
import uvicorn

#Other modules
from enum import Enum

#Creating the FastAPI instance
app = FastAPI()
client = TestClient(app)

#Initializing the application
storage = Storage()
irs_instance = IRS(storage)
selected_model = "None"

class ModelName(str, Enum):
    prob = "Probabilistic Model"
    vect = "Vector Space Model"
    lsi = "LSI Model"

class CollectionName(str, Enum):
    cran = "Cran"
    reuter = "Reuters"

class DocumentRank(BaseModel):
    id: int
    title: str
    body: str
    rank: float

@app.get("/api/model_options", response_model = list[str])
def get_model_options():
    return ["Vector Space Model", "Probabilistic Model", "LSI Model"]

@app.get("/api/collection_options", response_model = list[str])
def get_collection_options():
    return ["Cran", "Reuters"]

@app.get("/api/instantiated_models", response_model = list[str])
def get_instantiated_models():
    return irs_instance.list_models() 

@app.get("/api/selected_model", response_model = str)
def get_selected_model():
    return selected_model

@app.get("/api/query", response_model = tuple[list[DocumentRank], int])
def make_query(
    query: str = Query(default=..., title="Query", description="A query to be used by the retrieval system", regex="^(?!\s*$).+"),
    limit: int = Query(default=10, title="Limit", description="The number of documents from the ranking to be returned"),
    offset: int = Query(default=0, title="offset", description="The number of documents from the ranking to be skipped"),
    summary_len: int = Query(default=-1, title="Summary Length", description="The number of characters from the document body to be returned")
):
    query.strip()
    documents = []
    ranking, total = irs_instance.get_ranking(query, selected_model, limit, offset)#TODO: add offset
    return ([DocumentRank(id=doc[0], title=doc[1], body=doc[2][: None if summary_len == -1 else summary_len], rank = doc[3]) for doc in ranking], total)
    
    #[ ] bprrar esto
    for doc in ranking:
        documents.append(Document(id=doc[0], title=doc[1], body=doc[3][: None if summary_len == -1 else summary_len]))
    return documents

@app.get("/api/query/pseudo-feedback", response_model = list[DocumentRank])
def pseudo_feedback(
    query: str = Query(default=..., title="Query", description="A query to be used by the retrieval system", regex="^(?!\s*$).+"),
    limit: int = Query(default=10, title="Limit", description="The number of documents from the ranking to be returned"),
    offset: int = Query(default=0, title="offset", description="The number of documents from the ranking to be skipped"),
    summary_len: int = Query(default=-1, title="Summary Length", description="The number of characters from the document body to be returned")
):
    #[ ] borrar esto
    global irs_instance
    irs_instance = IRS(Storage())
    global selected_model
    selected_model = None
    
    query.strip()
    documents = []
    irs_instance.models[selected_model].pseudo_feedback(query)
    ranking = irs_instance.get_ranking(query, selected_model, limit, offset)#TODO: add offset
    return [DocumentRank(id=doc[0], title=doc[1], body=doc[2][: None if summary_len == -1 else summary_len], rank = doc[3]) for doc in ranking]

    #[ ] borrar esto
    for doc in ranking:
        documents.append(Document(id=doc[0], title=doc[1], body=doc[3][: None if summary_len == -1 else summary_len]))
    return documents

@app.post("/api/select_model/{model_name}", response_model = str)
def select_model(
     model_name: ModelName = Path(default=..., title="Model", description="The model to be used for processing the query"),
     collection_list: list[CollectionName] = Body(default=..., title="Collection List", description="The list of collections to be used for processing the query")
    ):
    global irs_instance
    irs_instance = IRS(Storage())
    global selected_model
    selected_model = None
    #TODO: What happens if i add new documents to an already instantiated model?
    model = None
    if model_name == ModelName.prob and model_name not in irs_instance.list_models():
        model = probabilistic_model.Probabilistic_Model(utils.processing_text)
    elif model_name == ModelName.vect and model_name not in irs_instance.list_models():
        model = vector_space_model.Vector_Model(utils.processing_text)
    elif model_name == ModelName.lsi and model_name not in irs_instance.list_models():
        model = lsi_model.LSI_Model(utils.processing_text)
    else:
        return {"Error": "Invalid model selected"}

    irs_instance.add_model(model)

    loaded_collection_parsers = irs_instance.list_parsers()
    collection_parsers = []
    for collection in collection_list:
        if collection == CollectionName.cran and collection not in loaded_collection_parsers:
            irs_instance.add_parser(CranParser(utils.processing_text))
            irs_instance.add_document_collection("./data", collection, model.get_name())
        elif collection == CollectionName.reuter and collection not in loaded_collection_parsers:
            irs_instance.add_parser(ReutersParser(utils.processing_text))
            irs_instance.add_document_collection("./data", collection, model.get_name())
    
    selected_model = model.get_name()
    return "Model instantiated correctly"

@app.get("/api/clear", status_code=204)
def clear():
    global irs_instance
    irs_instance = IRS(Storage())
    global selected_model
    selected_model = None
    return {}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)