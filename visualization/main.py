import urllib.request, json
import altair as alt
import pandas as pd
import geopandas as gpd

with urllib.request.urlopen("http://localhost:5000/vaccines/date?limit=1000") as url:
    vaccines_per_day = json.loads(url.read())

df = pd.DataFrame(vaccines_per_day).rename(columns={"firstdosequantity": "Primera Dosis", "seconddosequantity": "Segunda Dosis", "totalvaccines": "Total"})

areaPlot = alt.Chart(df, title='Vacunados por día')\
    .mark_area()\
    .transform_fold(['Primera Dosis', 'Segunda Dosis'], as_=['Dosis', 'Vacunados'])\
    .encode(x=alt.X('date:T', title='Fecha de Aplicación'), y='Vacunados:Q', color=alt.Color('Dosis:N',
              scale=alt.Scale(domain=['Primera Dosis','Segunda Dosis'], range=['#ffa600','#006400'])), 
            tooltip=[alt.Tooltip('date:T', title='Fecha de Aplicación'), 'Dosis:N', alt.Tooltip('Vacunados:Q', title='Vacunados'), 
            alt.Tooltip('Total:Q', title='Total Vacunados')])\
    .properties(width=1000)

with urllib.request.urlopen("http://localhost:5000/vaccines/province?limit=1000") as url:
    vaccines_per_province = json.loads(url.read())

province_df = gpd.read_file("./provincias_poligon.geo.json")
data_df = pd.DataFrame(vaccines_per_province).rename(columns={"firstdosequantity": "Primera Dosis", "seconddosequantity": "Segunda Dosis", "totalvaccines": "Total"})
merge_df = province_df.merge(data_df, left_on='provincia', right_on='province')

choro_json = json.loads(merge_df.to_json())
choro_data = alt.Data(values=choro_json['features'])

choropleth = alt.Chart(choro_data, title='Vacunados por provincia')\
    .mark_geoshape(stroke='black',strokeWidth=1)\
    .encode(color=alt.Color("properties['Total']", type='quantitative', scale=alt.Scale(scheme='bluegreen', type='log'), title = 'Total'),
            tooltip=[alt.Tooltip("properties['province']:N", title='Provincia'), alt.Tooltip("properties['Primera Dosis']:Q", title='Vacunados Primera Dosis'), 
                     alt.Tooltip("properties['Segunda Dosis']:Q", title='Vacunados Segunda Dosis'), alt.Tooltip("properties['Total']:Q", title='Total Vacunados')])\
    .properties(height=500)

bar_chart = alt.Chart(data_df, title='Vacunados por provincia')\
    .mark_bar()\
    .transform_fold(['Primera Dosis', 'Segunda Dosis'], as_=['Dosis', 'Vacunados'])\
    .encode(x='Vacunados:Q', y=alt.Y('province:N', sort='-x'), color=alt.Color('Dosis:N', scale=alt.Scale(domain=['Primera Dosis','Segunda Dosis'], range=['#ffa600','#006400'])),
            tooltip=[alt.Tooltip('Vacunados:Q', title='Vacunados'), alt.Tooltip('Total:Q', title='Total Vacunados')])

with urllib.request.urlopen("http://localhost:5000/type?limit=1000") as url:
    type_vaccine = json.loads(url.read())

df = pd.DataFrame(type_vaccine).rename(columns={"name": "Tipo", "vaccinequantity": "Cantidad"})
total = df['Cantidad'].sum()
df["Porcentaje"] = df["Cantidad"] / total

bar_chart_type = alt.Chart(df, title='Tipos de vacunas')\
    .mark_bar()\
    .encode(x=alt.X('Cantidad:Q', axis=None), color=alt.Color('Tipo:N', legend=alt.Legend(orient='top', direction="horizontal")), 
            tooltip=[alt.Tooltip('Cantidad:Q', title='Cantidad de vacunas'), alt.Tooltip('Porcentaje:Q', title='Porcentaje', format='.1%')])\
    .properties(width=1000)

with urllib.request.urlopen("http://localhost:5000/condition?limit=1000") as url:
    condition_vaccine = json.loads(url.read())

df = pd.DataFrame(condition_vaccine).rename(columns={"name": "Condicion", "vaccinequantity": "Cantidad"})
total = df['Cantidad'].sum()
df["Porcentaje"] = df["Cantidad"] / total

bar_chart_condition = alt.Chart(df, title='Codiciones de personas vacunadas')\
    .mark_bar()\
    .encode(x=alt.X('Cantidad:Q', axis=None), color=alt.Color('Condicion:N', legend=alt.Legend(orient='top', direction="horizontal", columns=5, labelLimit=300)), 
            tooltip=[alt.Tooltip('Cantidad:Q', title='Cantidad de vacunas'), alt.Tooltip('Porcentaje:Q', title='Porcentaje', format='.1%')])\
    .properties(width=1000)

dashboard = (areaPlot & (choropleth | bar_chart) & bar_chart_type & bar_chart_condition)\
    .resolve_scale(color='independent')\
    .configure_view(stroke=None)

dashboard.show()
