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
   northHemWA=w_avg(new_spatial.loc[new_spatial['LON']>23], days+10, 'AREA')
   southHemWA=w_avg(new_spatial.loc[new_spatial['LON']<-23], days+10, 'AREA')
   tropWA=w_avg(new_spatial.loc[abs(new_spatial['LON'])<23], days+10, 'AREA')
   northHemWP=w_avg(new_spatial.loc[new_spatial['LON']>23], days+10, 'POP2005')
   southHemWP=w_avg(new_spatial.loc[new_spatial['LON']<-23], days+10, 'POP2005')
   tropWP=w_avg(new_spatial.loc[abs(new_spatial['LON'])<23], days+10, 'POP2005')
   rows.append([northHemWA,southHemWA,tropWA,northHemWP,southHemWP,tropWP])
weight_avg=pd.DataFrame(rows, columns=["NorthHemByArea", "SouthHemByArea", "TropicalByArea", "NorthHemByPop", "SouthHemByPop", "TropicalByPop"])
ArtBA=weight_avg['NorthHemByArea'].mean()
AntBA=weight_avg['SouthHemByArea'].mean()
TroBA=weight_avg['TropicalByArea'].mean()
ArtBP=weight_avg['NorthHemByPop'].mean()
AntBP=weight_avg['SouthHemByPop'].mean()
TroBP=weight_avg['TropicalByPop'].mean()
newrows=[]
newrows.append(["Average",ArtBA,AntBA,TroBA,ArtBP,AntBP,TroBP])
ArtBAS=weight_avg['NorthHemByArea'].std()
AntBAS=weight_avg['SouthHemByArea'].std()
TroBAS=weight_avg['TropicalByArea'].std()
ArtBPS=weight_avg['NorthHemByPop'].std()
AntBPS=weight_avg['SouthHemByPop'].std()
TroBPS=weight_avg['TropicalByPop'].std()
newrows.append(["Standard Deviation",ArtBAS,AntBAS,TroBAS,ArtBPS,AntBPS,TroBPS])
avgAndStd=pd.DataFrame(newrows, columns=["Table 1: Average Temperature for Various Regions Weighted by Area and Population", "North Hemisphere By Area (C)", "South Hemisphere By Area (C)", "Tropical By Area (C)", "North Hemisphere By Area (C)", "South Hemisphere By Area (C)", "TropicalByPop"])
avgAndStd.to_csv('avgAndStd.csv', index=False)