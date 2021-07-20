from sqlalchemy.orm import Session
from persistence.database import engine
from sqlalchemy import text

from . import models

def get_information(db: Session, offset: int, limit: int):
    res = db.execute(
        "select last_update as lastUpdate\
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

def get_vaccines_per_province(db: Session, offset: int, limit: int):
    res = db.execute(
        "with primerasDosis as (\
            select jurisdiccion_aplicacion, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 1 and fecha_aplicacion != 'S.I.'\
            group by jurisdiccion_aplicacion\
        ),\
        segundasDosis as (\
            select jurisdiccion_aplicacion, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 2 and fecha_aplicacion != 'S.I.'\
            group by jurisdiccion_aplicacion\
        )\
        select primerasDosis.jurisdiccion_aplicacion as province, primerasDosis.totalVacunas as firstDoseQuantity, segundasDosis.totalVacunas as secondDoseQuantity, primerasDosis.totalVacunas + segundasDosis.totalVacunas as totalVaccines\
        from primerasDosis join segundasDosis on primerasDosis.jurisdiccion_aplicacion = segundasDosis.jurisdiccion_aplicacion\
        limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_provinces(db: Session, offset: int, limit: int):
    res = db.execute(
        "select jurisdiccion_aplicacion as name, count(*) as vaccineQuantity\
         from nomivac_covid19\
         group by jurisdiccion_aplicacion\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_by_province(db: Session, province: str, offset: int, limit: int):
    res = db.execute(
        "select sexo as sex, jurisdiccion_aplicacion as province, condicion_aplicacion as condition, vacuna as vaccine, lote_vacuna as lot\
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

def get_types(db: Session, offset: int, limit: int):
    res = db.execute(
        "select vacuna as name, count(*) as vaccineQuantity\
         from nomivac_covid19\
         group by vacuna\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_by_type(db: Session, vaccine_type: str, offset: int, limit: int):
    res = db.execute(
        "select sexo as sex, jurisdiccion_aplicacion as province, condicion_aplicacion as condition, vacuna as vaccine, lote_vacuna as lot\
         from nomivac_covid19\
         where vacuna = '" + vaccine_type + "'\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_per_day_by_type(db: Session, vaccine_type: str, offset: int, limit: int):
    res = db.execute(
        "with primerasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 1 and fecha_aplicacion != 'S.I.' and vacuna = '" + vaccine_type + "'\
            group by fecha_aplicacion\
        ),\
        segundasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 2 and fecha_aplicacion != 'S.I.' and vacuna = '" + vaccine_type + "'\
            group by fecha_aplicacion\
        )\
        select primerasDosis.fecha_appl as date, primerasDosis.totalVacunas as firstDoseQuantity, segundasDosis.totalVacunas as secondDoseQuantity, primerasDosis.totalVacunas + segundasDosis.totalVacunas as totalVaccines\
        from primerasDosis join segundasDosis on primerasDosis.fecha_appl = segundasDosis.fecha_appl\
        limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_conditions(db: Session, offset: int, limit: int):
    res = db.execute(
        "select condicion_aplicacion as name, count(*) as vaccineQuantity\
         from nomivac_covid19\
         group by condicion_aplicacion\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_by_condition(db: Session, condition: str, offset: int, limit: int):
    res = db.execute(
        "select sexo as sex, jurisdiccion_aplicacion as province, condicion_aplicacion as condition, vacuna as vaccine, lote_vacuna as lot\
         from nomivac_covid19\
         where condicion_aplicacion = '" + condition + "'\
         limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()

def get_vaccines_per_day_by_condition(db: Session, condition: str, offset: int, limit: int):
    res = db.execute(
        "with primerasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 1 and fecha_aplicacion != 'S.I.' and condicion_aplicacion = '" + condition + "'\
            group by fecha_aplicacion\
        ),\
        segundasDosis as (\
            select to_date(fecha_aplicacion, 'yyyy-MM-dd') as fecha_appl, count(*) as totalVacunas\
            from nomivac_covid19\
            where orden_dosis = 2 and fecha_aplicacion != 'S.I.' and condicion_aplicacion = '" + condition + "'\
            group by fecha_aplicacion\
        )\
        select primerasDosis.fecha_appl as date, primerasDosis.totalVacunas as firstDoseQuantity, segundasDosis.totalVacunas as secondDoseQuantity, primerasDosis.totalVacunas + segundasDosis.totalVacunas as totalVaccines\
        from primerasDosis join segundasDosis on primerasDosis.fecha_appl = segundasDosis.fecha_appl\
        limit " + str(limit) + " offset " + str(offset)
    )
    return res.mappings().all()
