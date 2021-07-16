create table nomivac_covid19(
    id serial primary key,
    sexo text,
    grupo_etario text,
    jurisdiccion_residencia text,
    jurisdiccion_residencia_id text,
    depto_residencia text,
    depto_residencia_id text,
    jurisdiccion_aplicacion text,
    jurisdiccion_aplicacion_id text,
    depto_aplicacion text,
    depto_aplicacion_id text,
    fecha_aplicacion text,
    vacuna text,
    condicion_aplicacion text,
    orden_dosis integer,
    lote_vacuna text
);

create table information (
    last_update timestamp
);