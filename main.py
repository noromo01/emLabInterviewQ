from xml.sax.xmlreader import AttributesImpl
import pandas as pd
country_geospatial = pd.read_csv("country_geospatial.csv", encoding  =  "ISO-8859-1")
country_dailyavg = pd.read_csv("country_dailyavg_ERA5_tavg_2015.csv", encoding = "ISO-8859-1")
new_spatial=pd.merge(country_geospatial,country_dailyavg, left_on='ISO3', right_on='iso3')
def w_avg(df, values, weights):
    d = df.iloc[:,values]
    w = df[weights]
    return (d * w).sum() / w.sum()
rows=[]
for days in range(365):
   a=w_avg(new_spatial.loc[new_spatial['LON']>23], days+10, 'AREA')
   b=w_avg(new_spatial.loc[new_spatial['LON']<-23], days+10, 'AREA')
   c=w_avg(new_spatial.loc[abs(new_spatial['LON'])<23], days+10, 'AREA')
   d=w_avg(new_spatial.loc[new_spatial['LON']>23], days+10, 'POP2005')
   e=w_avg(new_spatial.loc[new_spatial['LON']<-23], days+10, 'POP2005')
   f=w_avg(new_spatial.loc[abs(new_spatial['LON'])<23], days+10, 'POP2005')
   rows.append([a,b,c,d,e,f])
weight_avg=pd.DataFrame(rows, columns=["ArticByArea", "AntarticByArea", "TropicalByArea", "ArticByPop", "AntarticByPop", "TropicalByPop"])
ArtBA=weight_avg['ArticByArea'].mean()
AntBA=weight_avg['AntarticByArea'].mean()
TroBA=weight_avg['TropicalByArea'].mean()
ArtBP=weight_avg['ArticByPop'].mean()
AntBP=weight_avg['AntarticByPop'].mean()
TroBP=weight_avg['TropicalByPop'].mean()
newrows=[]
newrows.append(["Average",ArtBA,AntBA,TroBA,ArtBP,AntBP,TroBP])
ArtBAS=weight_avg['ArticByArea'].std()
AntBAS=weight_avg['AntarticByArea'].std()
TroBAS=weight_avg['TropicalByArea'].std()
ArtBPS=weight_avg['ArticByPop'].std()
AntBPS=weight_avg['AntarticByPop'].std()
TroBPS=weight_avg['TropicalByPop'].std()
newrows.append(["Std",ArtBAS,AntBAS,TroBAS,ArtBPS,AntBPS,TroBPS])
avgAndStd=pd.DataFrame(newrows, columns=["Titles", "ArticByArea", "AntarticByArea", "TropicalByArea", "ArticByPop", "AntarticByPop", "TropicalByPop"])
avgAndStd.to_csv('avgAndStd.csv', index=False)