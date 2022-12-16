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

#Algo como esto puede que se puedan usa varias colecciones y modelos a la vez
# class Query(BaseModel):
#     query: str
#     model: ModelName
#     collection: CollectionName

'''
Application Workflow:
[x] Initialize the IR System
 [x] Instantiate the storage
 [x] Instantiate the IRS module
[x] User defines data collection // TODO: If theres enough time, implement 
a way to receive the data collection directory
[x] User defines model
 [x] Model is instantiated with text preprocessor // TODO: Discuss 
 if we should instantiate the model with the preprocessor
 [x] Parser is instantiated with text preprocessor
[x] Finish IRS initialization
 [x] Add model to IRS
 [x] Add parser to IRS
[x] Add collection to IRS // TODO: If this collection is already in 
cache then it should be loaded from there (ask for cache format)

Asynchronous functionalities:
[ ] POST: Query
[ ] GET: Documents
[ ] GET: Collection and model selection // If theres already a different 
collection/model selected then it should be replaced
[ ] return some documents preview

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

class DocumentWithBody(Document):
    body: str

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

@app.get("/api/query", response_model=list[Document | DocumentWithBody])
def query(
    query: str = Query(default=..., title="Query", description="A query to be used by the retrieval system"),
    limit: int = Query(default=10, title="Limit", description="The number of documents from the ranking to be returned"),
    #offset: int = Query(default=0, title="Offset", description="The number of documents from the ranking to be skipped"),
    model_name: ModelName = Query(default=..., title="Model", description="The model to be used for processing the query")
    ):
    query.strip()
    if query == '':
        return {"Error": "Query is empty"}

    documents = []
    #TODO: I must limit the models clients can send so they can't send a model that is not in the IRS
    ranking = irs_instance.get_ranking(query, model_name, limit)
    for doc in ranking:
        documents.append(Document(id=doc[0], title=doc[1]))
    
    return documents

#TODO: This does not work yet
@app.get("/api/document/{id}", response_model=DocumentWithBody)
def get_document(
    id: int = Path(..., title="Document ID", description="The ID of the document to be returned")):
    document = irs_instance.get_document(id)
    return DocumentWithBody(id=document[0], title=document[1], body=document[2])

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
