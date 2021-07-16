from persistence.database import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class NomivacCovid19(Base):

    __tablename__ = "nomivac_covid19"

    id = Column(Integer, primary_key=True)
    sexo = Column(String)
    grupo_etario = Column(String)
    jurisdiccion_residencia = Column(String)
    jurisdiccion_residencia_id = Column(String)
    depto_residencia = Column(String)
    depto_residencia_id = Column(String)
    jurisdiccion_aplicacion = Column(String)
    jurisdiccion_aplicacion_id = Column(String)
    depto_aplicacion = Column(String)
    depto_aplicacion_id = Column(String)
    fecha_aplicacion = Column(String)
    vacuna = Column(String)
    condicion_aplicacion = Column(String)
    orden_dosis = Column(Integer)
    lote_vacuna = Column(String)