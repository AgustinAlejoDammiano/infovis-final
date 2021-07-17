from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import Optional
from persistence import queries
from persistence.database import SessionLocal, engine
import requests, zipfile, io
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/information/")
def get_information(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_information(db, offset, limit)

@app.get("/vaccines")
def vaccines(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines(db, offset, limit)

@app.get("/vaccines/date")
def vaccines_per_day(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_per_day(db, offset, limit)

@app.get("/vaccines/province")
def vaccines_per_province(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_per_province(db, offset, limit)

@app.get("/province/")
def provinces(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_provinces(db, offset, limit)

@app.get("/province/{province}/vaccines")
def vaccines_by_province(province: str, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_by_province(db, province, offset, limit)

@app.get("/province/{province}/vaccines/date")
def vaccines_per_day_by_province(province: str, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_per_day_by_province(db, province, offset, limit)

@app.post("/update/", responses={512: {"model": Message}})
def update():
    url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/datos_nomivac_covid19.zip'
    try:
        r = requests.get(url)
    except:
        return JSONResponse(status_code=512, content={"message": "Cannot connect to '" + url + "'"})
    if (not r.ok):
        return JSONResponse(status_code=512, content={"message": "Cannot connect to '" + url + "'"})
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("./")
    with open('./datos_nomivac_covid19.csv', 'r') as f, SessionLocal() as db:
        deleteConnection = engine.connect()
        deleteConnection.execute("delete from nomivac_covid19")
        deleteConnection.close()
        insertConnection = engine.raw_connection()
        cursor = insertConnection.cursor()
        cmd = "COPY nomivac_covid19(sexo,\
                grupo_etario,\
                jurisdiccion_residencia,\
                jurisdiccion_residencia_id,\
                depto_residencia,\
                depto_residencia_id,\
                jurisdiccion_aplicacion,\
                jurisdiccion_aplicacion_id,\
                depto_aplicacion,\
                depto_aplicacion_id,\
                fecha_aplicacion,\
                vacuna,\
                condicion_aplicacion,\
                orden_dosis,\
                lote_vacuna) FROM STDIN CSV DELIMITER ',' HEADER"
        cursor.copy_expert(cmd, f)
        insertConnection.commit()
        insertConnection.close()
        insertConnection = engine.connect()
        insertConnection.execute("insert into information values(NOW()::timestamp)")
        insertConnection.close()
        