from sqlalchemy.orm import Session
from persistence.database import engine
from sqlalchemy import text

from . import models

def get_information(db: Session):
    res = db.execute(
        "select *\
         from information\
         order by last_update DESC"
    )
    return res.mappings().all()

def get_vaccines_per_day(db: Session):
    
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
        from primerasDosis join segundasDosis on primerasDosis.fecha_appl = segundasDosis.fecha_appl;"\
    )

    return res.mappings().all()

