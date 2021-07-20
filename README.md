# infovis-final

El repositorio consiste de una api que provee datos sobre la vacunacion de Argentina y una visualización de la misma.

## Api

Para correr la api es necesario realizar los siguentes pasos, en el directorio de la misma:

```bash
sudo apt install postgresql postgresql-contrib
```

Crear una base de datos llamada vacunas que este en el puerto 5432. El usuario que tiene permissos se llame postgres con contraseña postgres. O cambiar estos datos en el archivo database.py. La base tiene que tener el esquema descripto por el archivo db.init.sql.

Luego ejecutar el siguiente comando para installar los requisitos de la api:

```bash
pip install -r requirements.txt
```

El siguiente paso es poblar la api. Esto se puede hacer por medio de endpoint de update, pero se recomienda usar el siguiente comando ya que es mas rapido (habiendo descargado el csv con los datos y nombrandolo datos_nomivac_covid19.csv):


```bash
sudo -u postgres psql -c "\copy nomivac_covid19(sexo, grupo_etario, jurisdiccion_residencia, jurisdiccion_residencia_id, depto_residencia, depto_residencia_id, jurisdiccion_aplicacion, jurisdiccion_aplicacion_id, depto_aplicacion, depto_aplicacion_id, fecha_aplicacion, vacuna, condicion_aplicacion, orden_dosis, lote_vacuna) from './datos_nomivac_covid19.csv' delimiter ',' csv header" -U postgres -d vacunas
```

Finalmentes se puede correr la api con el comando (el puerto puede cambiarse):

```bash
uvicorn main:app --port 5000
```

La documentacion de los endpoints se encuentra en la url http://localhost:5000/docs

## Visualización

Para correr la api es necesario realizar los siguentes pasos, en el directorio de la misma:

```bash
pip install -r requirements.txt
python main.py 
```