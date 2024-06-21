from contextlib import asynccontextmanager
from typing import Union
import random
from databases import Database
from fastapi import FastAPI, status, Response, responses
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
    asyncio.create_task(read_bluetooth(db))
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

@app.get('/')
def base_route():
    response = responses.RedirectResponse(url='/docs')
    return response


@app.post('/percurso/iniciar')
async def percurso_iniciar(response: Response):
    """
    Inicia um novo percurso e envia uma requisição para o carrinho para iniciar a sua trajetória.
    """
    has_active_percurso = "SELECT idPercurso from percurso WHERE ativo = 1"
    active_percurso = await db.fetch_one(has_active_percurso)
    if active_percurso is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"Já existe um percurso iniciado. Finalize o percurso antes de iniciar um novo"
    create_percurso = "INSERT INTO percurso DEFAULT VALUES"
    data = await db.execute(create_percurso)
    print(data)
    write_bluetooth(1)
    return {'idPercurso': data, 'message': 'percurso inicado'} 

@app.put('/percurso/finalizar')
async def percurso_finalizar():
    find_active_percurso = "SELECT idPercurso from percurso WHERE ativo = 1"
    active_percurso = await db.fetch_one(find_active_percurso)
    deactivate_percurso = f'UPDATE percurso SET ativo=0 WHERE idPercurso = {active_percurso}'
    await db.execute(deactivate_percurso)
    write_bluetooth(0)
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
