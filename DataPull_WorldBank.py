import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import seaborn
import seaborn as sns
import quandl

# set quandl API key
quandl.ApiConfig.api_key = "1wrL_b1e1tDUP57ekYP8"
# get the world bank data for Ireland along with the World bank meta data courtesy of data.nasdaq.com
q_data = quandl.get_table('WB/DATA?country_code=IRL', paginate=True)
q_meta_data = quandl.get_table('WB/METADATA', paginate=True)
meta_data = q_meta_data[["series_id", "name"]]
merged_data = q_data.merge(meta_data, on="series_id")

Ireland_1990 = merged_data[np.logical_and(merged_data["year"]>= 1990, merged_data["year"]<= 2015)]
Ireland_1990_clean = Ireland_1990.drop(labels=["country_code","country_name"], axis=1, inplace=False)

cols_to_keep = ["TX.VAL.MRCH.XD.WD", "TM.VAL.MRCH.XD.WD", "ST.INT.DPRT", "SP.POP.TOTL", "SP.POP.65UP.TO", "SP.DYN.TFRT.IN", "SP.DYN.LE00.IN", "SM.POP.REFG", "SL.UEM.TOTL.NE.ZS",
                "SL.TLF.TOTL.IN","SL.SRV.EMPL.ZS", "SL.GDP.PCAP.EM.KD", "SH.MED.BEDS.ZS", "SE.XPD.TOTL.GD.ZS", "NY.GNP.PCAP.PP.CD", "IT.CEL.SETS.P2","GC.TAX.TOTL.CN",
                "GC.DOD.TOTL.CN", "EN.ATM.GHGT.KT.CE", "AG.LND.ARBL.HA", "AG.CON.FERT.ZS"]
Ireland_1990_final= Ireland_1990_clean[Ireland_1990_clean["series_id"].isin(cols_to_keep)]
Ireland_1990_final.reset_index(drop= True, inplace= True)
Ireland_1990_final.to_csv("D:\My Documents\Downloads\Ireland_1990_final.csv")

# print(Ireland_1990_final.pivot_table(values="value", index="series_id", columns="year", fill_value=0, margins=True))
Ireland_1990_pivot1= Ireland_1990_final.pivot_table(values="value", index="series_id", columns="year", fill_value=0)
Ireland_1990_pivot2= Ireland_1990_final.pivot_table(values="value", index="series_id", fill_value=0, aggfunc= [np.mean, np.median, np.std, np.max, np.min])
Ireland_1990_pivot1.to_csv("D:\My Documents\Downloads\Ireland_1990_pivot1.csv")
Ireland_1990_pivot2.to_csv("D:\My Documents\Downloads\Ireland_1990_pivot2.csv")
Ireland_pivot_merge= Ireland_1990_pivot1.merge(Ireland_1990_pivot2, on="series_id")
Ireland_pivot_merge.to_csv("D:\My Documents\Downloads\Ireland_pivot_merge.csv")

Ireland_GDP= Ireland_1990_final[Ireland_1990_final["series_id"]=="SL.GDP.PCAP.EM.KD"]
Ireland_GDP.to_csv("D:\My Documents\Downloads\Ireland_GDP.csv")
print(Ireland_GDP.info())
print(Ireland_GDP.shape)


Ireland_GDP_pivot = Ireland_GDP.pivot_table(values="value", index="year", columns="series_id", fill_value=0)
Ireland_GDP_pivot.to_csv("D:\My Documents\Downloads\Ireland_GDP_pivot.csv")
print(Ireland_GDP_pivot.info)
#x= Ireland_GDP["year"]
#y= Ireland_GDP["value"]
Ireland_GDP.plot(kind='scatter', x='year', y='value')

#Sample Graph
#price_diffs.plot(y=['close_jpm','close_wells','close_bac'])
#Same result
#price_diffs.plot(kind='line',x='date_time',y=['close_jpm','close_wells','close_bac'])
#another sample
#gdp_recession.plot(kind='bar', y='gdp', x='date', rot=90)



#plt.show()


plt.show()
#Ireland_GDP_pivot.plot(kind='scatter', x='year', y='SL.GDP.PCAP.EM.KD')
#plt.show()
#sns.scatterplot(x=Ireland_GDP["year"], y=Ireland_GDP["value"])
#plt.show()

#sns.scatterplot(x=Ireland_GDP_pivot["year"], y=Ireland_GDP_pivot["SL.GDP.PCAP.EM.KD"])
#plt.show()