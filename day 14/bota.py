
import plotly.express as px
import panda as pd
import matplotlib.pyplot as pit

df = pd.read_csv("avgIQpercountry.csv")

df['Population - 2023']= df['Population - 2023'].str.replace(',','').astype(float)

print(df.info())

fig = px.scatter_geo(df,location='Country',locationode='Country names',
                     over_name='Country',size="Avarage IQ",color="Continent",
                     projection='natural earth',title='Avarage IQ by Country',
                     size_max=20,template='plotly_dark')
