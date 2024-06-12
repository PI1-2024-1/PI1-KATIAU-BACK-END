from contextlib import asynccontextmanager
from typing import Union
import random
from fastapi import FastAPI, APIRouter
from databases import Database

DATABASE_URL="sqlite:///./mydb.db"
db = Database(DATABASE_URL)

global idPercurso
idPercurso = 0
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



@app.post('/percurso/iniciar')
def percurso_iniciar():
    """
    Inicia um novo percurso e envia uma requisição para o carrinho para iniciar a sua trajetória.
    """
    idPercurso= random.randint(1, 20)
    return {'idPercurso': idPercurso, 'message': 'percurso inicado'} 

@app.put('/percurso/finalizar')
def percurso_finalizar():
    return {'message': 'percurso finalizado'}



"""
    IMPORTANTE: ABAIXO TEMOS ALGUNS EXEMPLOS DE QUERIES E DE COMO UTILIZAR O FASTAPI PARA FAZER APIs
"""
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

@app.post('carrinho')
async def toggle_carrinho():
    ...
    ...

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    ...


@app.get("percurso/")
def get_percursos():
    # pegar todos os percursos para calcular a dist percorrida e tempo decorrido