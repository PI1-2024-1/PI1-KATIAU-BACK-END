from contextlib import asynccontextmanager
from typing import Union
from sqlite3 import Connection
from fastapi import FastAPI, Depends
from databases import Database

DATABASE_URL="sqlite:///./mydb.db"
db = Database(DATABASE_URL)


@asynccontextmanager
async def connect_database(app: FastAPI):
    # Load the ML model
    print(f"Conectado ao banco de dados {DATABASE_URL}")
    await db.connect()
    yield
    # Clean up the ML models and release the resources
    await db.disconnect()
    print('Banco desconectado')
app = FastAPI(lifespan=connect_database)

@app.get("/")
async def create_table():
    await db.execute("CREATE TABLE movie(name, year, rate)")
    return "Created Table"


@app.get("/movie/create")
async def create_movie():
    await db.execute("INSERT INTO movie VALUES('movie1', 2023, 8)")
    
    return "Created movie"

@app.get("/movie/get")
async def get_movie():
    query = await db.fetch_all('SELECT * FROM movie')
    return query

@app.get('/user')
def get_user():
    return testfunc()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    ...