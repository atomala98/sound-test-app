from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient

app = FastAPI()


conn_str = 'mongodb+srv://andrzej:atatat12@audiofiles.56myc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(conn_str)
db = client["Audio-files"]
wav_collection = db["Audio-files"]


@app.get("/")
def root():
    # result = wav_collection.insert_one({'test': 'test'})
    return {'test': 'test1'}