from databases import Database

async def init_database(db: Database): 
    await db.connect()
    print(f"Conectado ao banco de dados {db.url}")
    
    
    await db.execute("""CREATE TABLE IF NOT EXISTS percurso(
        idPercurso INTEGER PRIMARY KEY AUTOINCREMENT, 
        distPercorrida FLOAT DEFAULT 0,
        tempoDecorrido FLOAT DEFAULT 0)""")
    await db.execute("""CREATE TABLE IF NOT EXISTS telemetria(
        idTelemetria INTEGER PRIMARY KEY AUTOINCREMENT, 
        idPercurso INTEGER NOT NULL,
        distTotal FLOAT,
        posX FLOAT,
        posY FLOAT,
        velocidade FLOAT,
        aceleracao FLOAT,
        corrente FLOAT,
        energia FLOAT,
        data TEXT,
        FOREIGN KEY (idPercurso) 
            REFERENCES percurso (idPercurso) 
                ON DELETE CASCADE 
                ON UPDATE NO ACTION)""")

