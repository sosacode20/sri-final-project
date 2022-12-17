#IRS modules
from src.irs import IRS
from src.models import vector_space_model, probabilistic_model
from src.model import Model
from src.storage import Storage
from src import utils
from src.irs_parser import CranParser, ReutersParser, Parser

#Web application modules
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

#For testing
import uvicorn

#Other modules
from enum import Enum

#Creating the FastAPI instance
app = FastAPI()

#Initializing the application
storage = Storage()
irs_instance = IRS(storage)
selected_model = "None"

'''

Application Workflow:
[x] User defines data collection // TODO: If theres enough time, implement 
a way to receive the data collection directory
 [x] Model is instantiated with text preprocessor // TODO: Discuss 
 if we should instantiate the model with the preprocessor
[x] Add collection to IRS // TODO: If this collection is already in 
cache then it should be loaded from there (ask for cache format)

New Functionalities with front in mind
[x] Getting instantiated Models
[ ] Getting collections from Models
[ ] Queries are only done in a model and collection specific
[ ] Getting ranked documents with offset

'''

class ModelName(str, Enum):
    prob = "Probabilistic Model"
    vect = "Vector Space Model"
    placeholder = "placeholder"

class CollectionName(str, Enum):
    cran = "cran"
    reuter = "reuter"
    placeholder = "placeholder"

class Document(BaseModel):
    id: int
    title: str
    body: str

'''
#TODO: Divide this in two different endpoints
@app.get("/api")
def set_model_collection(
    model_name: ModelName = Query(default=..., title="Model", description="The model to be used for the Information Retrieval System"),
    collection: CollectionName = Query(default=..., title="Collection", description="The collection to be used for the Information Retrieval System")
    ):
    #TODO: Remove this when its done
    model = None
    if model_name == ModelName.placeholder or collection == CollectionName.placeholder:
        return {"Error": "Model or collection not implemented yet"}  
    elif model_name == ModelName.prob:
        model = probabilistic_model.Probabilistic_Model(utils.processing_text)
    elif model_name == ModelName.vect:
        model = vector_space_model.Vector_Model(utils.processing_text)
    else:
        return {"Error": "Invalid model selected"}
    
    if collection == CollectionName.cran:
        parser = CranParser(utils.processing_text)
    elif collection == CollectionName.reuter:
        parser = ReutersParser(utils.processing_text)
    else:
        return {"Error": "Invalid collection selected"}
    
    irs_instance.add_model(model)
    irs_instance.add_parser(parser)

    #TODO: This should not be done if collection is already in cache
    irs_instance.add_document_collection("./data", parser.get_pretty_name(), model.get_name())
    return {"Message": "IRS initialized"}

#TODO: This does not work yet
@app.get("/api/document/{model_name}/{id}", response_model=Document)
def get_document(
    id: int = Path(..., 
     title="Document ID", description="The ID of the document to be returned"),
    model_name: ModelName = Path(default=..., 
     title="Model", description="The model to be used for processing the query")
    ):
    document = irs_instance.models[model_name].get_document_by_id(id)
    return Document(id=document.doc_id, title=document.doc_id, body=document.doc_body)

#####################################
#    New Back With Front in Mind    #
#####################################
'''


@app.get("/api/model_options", response_model = list[str])
def get_model_options():
    return ["Vectorial Space Model", "Probabilistic Model"]

@app.get("/api/collection_options", response_model = list[str])
def get_collection_options():
    return ["Cran", "Reuters"]

@app.get("/api/instantiated_models", response_model = list[str])
def get_instantiated_models():
    return irs_instance.list_models() 

@app.get("/api/selected_model", response_model = str)
def get_selected_model():
    return selected_model

#TODO: Return rating
@app.get("/api/query", response_model = list[Document])
def make_query(
    query: str = Query(default=..., title="Query", description="A query to be used by the retrieval system", regex="^(?!\s*$).+"),
    limit: int = Query(default=10, title="Limit", description="The number of documents from the ranking to be returned"),
    offset: int = Query(default=0, title="offset", description="The number of documents from the ranking to be skipped"),
    summary_len: int = Query(default=-1, title="Summary Length", description="The number of characters from the document body to be returned")
):
    query.strip()
    documents = []
    ranking = irs_instance.get_ranking(query, selected_model, limit)#TODO: add offset
    return [Document(id=doc[0], title=doc[1], body=doc[2][: None if summary_len == -1 else summary_len]) for doc in ranking]

    for doc in ranking:
        documents.append(Document(id=doc[0], title=doc[1], body=doc[3][: None if summary_len == -1 else summary_len]))
    return documents

@app.post("/api/select_model/{model_name}", response_model = str)
def select_model(
     model_name: ModelName = Path(default=..., title="Model", description="The model to be used for processing the query"),
     collection_list: list[CollectionName] = Body(default=..., title="Collection List", description="The list of collections to be used for processing the query")
    ):
    #TODO: What happens if i add new documents to an already instantiated model?
    model = None
    if model_name == ModelName.prob and model_name not in irs_instance.list_models():
        model = probabilistic_model.Probabilistic_Model(utils.processing_text)
    elif model_name == ModelName.vect and model_name not in irs_instance.list_models():
        model = vector_space_model.Vector_Model(utils.processing_text)
    else:
        return {"Error": "Invalid model selected"}

    collection_parsers = []
    for collection in collection_list:
        if collection == CollectionName.cran and collection not in irs_instance.list_parsers():
            collection_parsers.append(CranParser(utils.processing_text))
        elif collection == CollectionName.reuter and collection not in irs_instance.list_parsers():
            collection_parsers.append(ReutersParser(utils.processing_text))
        else:
            return {"Error": "Invalid collection selected"}
    
    irs_instance.add_model(model)
    for parser in collection_parsers:
        irs_instance.add_parser(parser)
        irs_instance.add_document_collection("./data", parser.get_pretty_name(), model.get_name())
    
    global selected_model 
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
























## Guide request for the API
class Item(BaseModel):
    query: str = Field(..., example="query")

@app.put("/items/{item_id}")
async def guide_endpoint(
    item_id: int = Path(),# Path parameter
    item: Item = Body(embed=True),# Body parameter
    q: str = Query(default = None, alias="item-query")# Query parameter
    ):
    results = {"item_id": item_id, "item": item, "query": item.query}
    return results
