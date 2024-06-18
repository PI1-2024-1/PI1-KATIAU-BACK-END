from contextlib import asynccontextmanager
from typing import Union
import random
from databases import Database
from fastapi import FastAPI, status, Response
import asyncio
import logger
from init_db import init_database
from bluetooth_connector import read_bluetooth, write_bluetooth
from fastapi.middleware.cors import CORSMiddleware


DATABASE_URL="sqlite:///./katiau.db"
db = Database(DATABASE_URL) 

# def bluetooth_reader_threaded_function(args):
#     """
#     Função que encapsula a função de  de bluetooth passando o contexto do banco de dados
#     """
    
#     read_bluetooth(args)
    

@asynccontextmanager
async def pre_init(app: FastAPI):
    await init_database(db)
    
    # Comente essa proxima linha caso necessário
    # asyncio.create_task(read_bluetooth(db))
    yield
    await db.disconnect()
    print('Banco desconectado')
app = FastAPI(lifespan=pre_init)

origins = [
    "http://localhost",
    "http://localhost:5173",  # Adicione aqui qualquer origem que você deseja permitir
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/percurso/")
async def get_percursos():
    # Execute a SELECT query to fetch all rows and specific columns
    query = "SELECT idPercurso, distPercorrida, tempoDecorrido FROM percurso"
    rows = await db.fetch_all(query)
    
    # Transform the data into a list of dictionaries
    data = []
    for row in rows:
        data.append({
            "idPercurso": row["idPercurso"],
            "distPercorrida": row["distPercorrida"],
            "tempoDecorrido": row["tempoDecorrido"]
        })
    
    # Return the data in JSON format
    return data

@app.get("/percurso/{idPercurso}/detalhes")
async def get_telemetria(idPercurso: int, response: Response, idTelemetria: int = None):
    find_percurso_query = f"SELECT idPercurso FROM percurso WHERE idPercurso={idPercurso}"
    percurso = await db.fetch_one(find_percurso_query)
    if percurso is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Percurso de id {idPercurso} não existe. Tente um outro id"
    
    list_telemetria = f"SELECT * FROM telemetria WHERE idPercurso={idPercurso} ORDER BY idTelemetria"
    if idTelemetria is not None:
        idTelemetria = int(idTelemetria)
        list_telemetria = f"SELECT * FROM telemetria WHERE idPercurso={idPercurso} AND idTelemetria > {idTelemetria} ORDER BY idTelemetria"
    rows = await db.fetch_all(list_telemetria)
    return rows

"""
    IMPORTANTE: ABAIXO TEMOS ALGUNS EXEMPLOS DE QUERIES E DE COMO UTILIZAR O FASTAPI PARA FAZER APIs
"""
# @app.get("/")
# async def create_table():
#     data = write_bluetooth(b'1')
#     return data

@app.get("/movie/create")
async def create_movie():
    await db.execute("INSERT INTO movie VALUES('movie1', 2023, 8)")
    
    return "Created movie"

@app.get("/movie/get")
async def get_movie():
    query = await db.fetch_all('SELECT * FROM percurso')
    return query

@app.post('carrinho')
async def toggle_carrinho():
    ...
    ...

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    ...


