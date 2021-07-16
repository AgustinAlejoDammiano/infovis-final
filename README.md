# infovis-final

pip requirements

sudo apt install postgresql postgresql-contrib

configure database

uvicorn main:app

sudo -u postgres psql -c "\copy nomivac_covid19(sexo, grupo_etario, jurisdiccion_residencia, jurisdiccion_residencia_id, depto_residencia, depto_residencia_id, jurisdiccion_aplicacion, jurisdiccion_aplicacion_id, depto_aplicacion, depto_aplicacion_id, fecha_aplicacion, vacuna, condicion_aplicacion, orden_dosis, lote_vacuna) from './datos_nomivac_covid19.csv' delimiter ',' csv header" -U postgres -d vacunas