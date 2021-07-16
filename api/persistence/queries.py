from sqlalchemy.orm import Session
from persistence.database import engine
from sqlalchemy import text

from . import models

def get_information(db: Session, offset: int, limit: int):
    res = db.execute(
        "select *\
         from information\
         order by last_update DESC \
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines(db: Session, offset: int, limit: int): 
    res = db.execute(
        "select sexo as sex, jurisdiccion_aplicacion as province, condicion_aplicacion as condition, vacuna as vaccine, lote_vacuna as lot \
         from nomivac_covid19\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_per_day(db: Session, offset: int, limit: int):
    res = db.execute(
        "with primerasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 1 and fecha_aplicacion != 'S.I.'\
            group by fecha_aplicacion\
        ),\
        segundasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 2 and fecha_aplicacion != 'S.I.'\
            group by fecha_aplicacion\
        )\
        select primerasDosis.fecha_appl as date, primerasDosis.totalVacunas as firstDoseQuantity, segundasDosis.totalVacunas as secondDoseQuantity, primerasDosis.totalVacunas + segundasDosis.totalVacunas as totalVaccines\
        from primerasDosis join segundasDosis on primerasDosis.fecha_appl = segundasDosis.fecha_appl\
        limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_provinces(db: Session, offset: int, limit: int):
    res = db.execute(
        "select jurisdiccion_aplicacion as name\
         from nomivac_covid19\
         group by jurisdiccion_aplicacion\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_by_province(db: Session, province: str, offset: int, limit: int):
    res = db.execute(
        "select *\
         from nomivac_covid19\
         where jurisdiccion_aplicacion = '" + province + "'\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_per_day_by_province(db: Session, province: str, offset: int, limit: int):
    res = db.execute(
        "with primerasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 1 and fecha_aplicacion != 'S.I.' and jurisdiccion_aplicacion = '" + province + "'\
            group by fecha_aplicacion\
        ),\
        segundasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 2 and fecha_aplicacion != 'S.I.' and jurisdiccion_aplicacion = '" + province + "'\
            group by fecha_aplicacion\
        )\
        select primerasDosis.fecha_appl as date, primerasDosis.totalVacunas as firstDoseQuantity, segundasDosis.totalVacunas as secondDoseQuantity, primerasDosis.totalVacunas + segundasDosis.totalVacunas as totalVaccines\
        from primerasDosis join segundasDosis on primerasDosis.fecha_appl = segundasDosis.fecha_appl\
        limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()