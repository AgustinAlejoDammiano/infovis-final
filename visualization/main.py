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
            tooltip=[alt.Tooltip("properties['province']:N", title='provincia'), alt.Tooltip("properties['Primera Dosis']:Q", title='Vacunados Primera Dosis'), 
                     alt.Tooltip("properties['Segunda Dosis']:Q", title='Vacunados Segunda Dosis'), alt.Tooltip("properties['Total']:Q", title='Total Vacunados')])

bar_chart = alt.Chart(data_df, title='Vacunados por provincia')\
    .mark_bar()\
    .transform_fold(['Primera Dosis', 'Segunda Dosis'], as_=['Dosis', 'Vacunados'])\
    .encode(x='Vacunados:Q', y=alt.Y('province:N', sort='-x'), color=alt.Color('Dosis:N', scale=alt.Scale(domain=['Primera Dosis','Segunda Dosis'], range=['#ffa600','#006400'])),
            tooltip=['Dosis:N', alt.Tooltip('Vacunados:Q', title='Vacunados'), alt.Tooltip('Total:Q', title='Total Vacunados')])

dashboard = alt.vconcat(areaPlot, choropleth, bar_chart)

dashboard.serve()
