from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27018")
db = client['e-comm-stream']
collection = db['trending']

@app.get("/debug")
def debug():
    return {
        "databases": client.list_database_names(),
        "collections": db.list_collection_names()
    }

# Get Trending Products
@app.get("/trending")
def get_trending():
    data = list(collection.find({}, {"_id":0}))
    print("Data from MongoDB:",data)
    return {"trending" : data}


# Get Recommended Products
@app.get("/recommended/{product_id}")
def get_trending(product_id: int):
    data = list(collection.find({"product_id":product_id}, {"_id":0}))
    return {"recommendations" : data}
