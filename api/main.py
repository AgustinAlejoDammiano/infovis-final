from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import Optional
from persistence import queries
from persistence.database import SessionLocal, engine
import requests, zipfile, io
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import date

tags = [
    {"name": "Database", "description": "Interact with the database."},
    {"name": "Vaccine", "description": "Endpoints aboute the vaccination."},
    {"name": "Province", "description": "Endpoints aboute the Province of Argentina."},
    {"name": "Type", "description": "Endpoints aboute the type of vaccine."},
    {"name": "Condition", "description": "Endpoints aboute the vaccination condition."}
]

app = FastAPI(
    title="Vaccines Argentina COVID19",
    description="API that provides information about the vacunation in Argentina for COVID19",
    openapi_tags=tags
)

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

class Information(BaseModel):
    information: str

class Date(BaseModel):
    date: date
    firstdosequantity: int
    seconddosequantity: int
    totalvaccines: int

class Province(BaseModel):
    province: str
    firstdosequantity: int
    seconddosequantity: int
    totalvaccines: int

class Vaccine(BaseModel):
    sex: str
    province: str
    condition: str
    vaccine: str
    lot: str

class Entity(BaseModel):
    name: str
    vaccinequantity: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/information/", tags=["Database"], response_model=List[Information])
def information(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_information(db, offset, limit)

@app.get("/vaccines", tags=["Vaccine"], response_model=List[Vaccine])
def vaccines(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines(db, offset, limit)

@app.get("/vaccines/date", tags=["Vaccine"], response_model=List[Date])
def vaccines_per_day(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_per_day(db, offset, limit)

@app.get("/vaccines/province", tags=["Vaccine"], response_model=List[Province])
def vaccines_per_province(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_per_province(db, offset, limit)

@app.get("/province/", tags=["Province"], response_model=List[Entity])
def provinces(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_provinces(db, offset, limit)

@app.get("/province/{province}/vaccines", tags=["Province"], response_model=List[Vaccine])
def vaccines_by_province(province: str, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_by_province(db, province, offset, limit)

@app.get("/province/{province}/vaccines/date", tags=["Province"], response_model=List[Date])
def vaccines_per_day_by_province(province: str, db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_vaccines_per_day_by_province(db, province, offset, limit)

@app.get("/type/", tags=["Type"], response_model=List[Entity])
def types(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_types(db, offset, limit)

@app.get("/condition/", tags=["Condition"], response_model=List[Entity])
def condition(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    return queries.get_conditions(db, offset, limit)

@app.post("/update/", responses={512: {"model": Message}}, tags=["Database"])
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
        