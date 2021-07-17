import urllib.request, json
import altair as alt
from altair.vegalite.v4.api import condition
from altair.vegalite.v4.schema.channels import Tooltip
import pandas as pd

with urllib.request.urlopen("http://localhost:5000/vaccines/date?limit=1000") as url:
    vaccines_per_day = json.loads(url.read())

df = pd.DataFrame(vaccines_per_day).rename(columns={"firstdosequantity": "Primera Dosis", "seconddosequantity": "Segunda Dosis", "totalvaccines": "Total"})

areaPlot = alt.Chart(df)\
    .mark_area()\
    .transform_fold(['Primera Dosis', 'Segunda Dosis'],
        as_=['Dosis', 'Vacunados'])\
    .encode(x=alt.X('date:T', title='Fecha de Aplicación'), y='Vacunados:Q', color=alt.Color('Dosis:N',
              scale=alt.Scale(domain=['Primera Dosis','Segunda Dosis'], range=['#ffa600','#006400'])), 
            tooltip=[alt.Tooltip('date:T', title='Fecha de Aplicación'), 'Dosis:N', alt.Tooltip('Vacunados:Q', title='Vacunados'), 
            alt.Tooltip('Total:Q', title='Total Vacunados')])\
    .properties(width=1000)

dashboard = alt.vconcat(areaPlot)

dashboard.serve()
