from databases import Database

async def init_database(): 
    
    DATABASE_URL="sqlite:///./katiau.db"
    db = Database(DATABASE_URL) 
    
    
    await db.connect()
    
    print(f"Conectado ao banco de dados {DATABASE_URL}")
    
    await db.execute("""CREATE TABLE IF NOT EXISTS percurso(
        idPercurso INTEGER PRIMARY KEY AUTOINCREMENT, 
        distPercorrida FLOAT DEFAULT 0,
        tempoDecorrido FLOAT DEFAULT 0)""")
    
    await db.execute("""CREATE TABLE IF NOT EXISTS telemetria(
        idTelemetria INTEGER PRIMARY KEY AUTOINCREMENT, 
        idPercurso FLOAT NOT NULL,
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

    
    return db

    
