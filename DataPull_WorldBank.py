#import the packages for use in the script
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl

# Change matplotlib parameters to ensure parameter names don't get truncated in the plots
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#Read data from data.nasdaq.com via an API
# set quandl API key as provided by the web site
quandl.ApiConfig.api_key = "1wrL_b1e1tDUP57ekYP8"
# get the world bank data for Ireland
q_data = quandl.get_table('WB/DATA?country_code=IRL', paginate=True)
# get the meta data for the world bank data above. Provides more infomatin on each parameter
q_meta_data = quandl.get_table('WB/METADATA', paginate=True)
#Just use the required columns from the meta data table
meta_data = q_meta_data[["series_id", "name"]]

#Merge the data with the meta data
merged_data = q_data.merge(meta_data, on="series_id").round(3)

#Use the .qeury method to filter the data to the years 1990 to 2015 inclusive
Ireland_1990 = merged_data.query('year >= 1990')

#Dropping these columns as they don't add any useful information
Ireland_1990_clean = Ireland_1990.drop(labels=["country_code","country_name"], axis=1, inplace=False)

#The data set contains a large bumber of different metrics.This creates a list of the metrics to keep from the data set
rows_to_keep = ["ST.INT.DPRT", "SP.POP.TOTL", "SP.POP.65UP.TO", "SP.DYN.LE00.IN",
                "SL.UEM.TOTL.NE.ZS","SL.TLF.TOTL.IN","SL.SRV.EMPL.ZS",
                "SL.GDP.PCAP.EM.KD", "SH.MED.BEDS.ZS", "NY.GNP.PCAP.PP.CD",
                "IT.CEL.SETS.P2","GC.TAX.TOTL.CN","EN.ATM.GHGT.KT.CE",
                "AG.CON.FERT.ZS"
                ]
Ireland_1990_final= Ireland_1990_clean[Ireland_1990_clean["series_id"].isin(rows_to_keep)]

#Adding a column with more informative names for each metric using a dictionary
indicator_description = {"ST.INT.DPRT":"Number Tourist Departures",
                  "SP.POP.TOTL":"Total Population",
                  "SP.POP.65UP.TO":"Total Population Over 65",
                  "SP.DYN.LE00.IN":"Life Expectancy at Birth",
                 "SL.UEM.TOTL.NE.ZS":"Unemployment as % of Work Force",
                  "SL.TLF.TOTL.IN":"Total Workforce",
                  "SL.SRV.EMPL.ZS":"% Workforce in Services Ind",
                  "SL.GDP.PCAP.EM.KD":"GDP per person employed",
                  "SH.MED.BEDS.ZS":"Hospital Beds per 1,000 people",
                  "NY.GNP.PCAP.PP.CD":"GNI per capita",
                  "IT.CEL.SETS.P2":"Mobile Subscriptions per 100 people",
                  "GC.TAX.TOTL.CN":"Total Tax revenue",
                  "EN.ATM.GHGT.KT.CE":"Greenhouse Gas (kt of CO2 equiv)",
                  "AG.CON.FERT.ZS" :"Fertilizer consumption (kg/hectare)"
                  }
Ireland_1990_final["Parameteric"] = Ireland_1990_final["series_id"].map(indicator_description)
print(type(Ireland_1990_final))
#save as .csv file if needed
Ireland_1990_final.to_csv("Ireland_1990_final.csv")

#Create statistical summary table with minimum, mean, maximum and standard deviation
group_Ireland_Parametric= Ireland_1990_final.groupby("Parameteric")["value"].agg(['min', 'mean', 'max', 'std']).round(3)
#save table as a csv for review if required.
group_Ireland_Parametric.to_csv('group_Ireland_Parametric.csv')

#Pivot the data to make it easier to read and save the table as .csv. THis table is used in the later plots
pivot_Ireland_EachParametricOverTime= Ireland_1990_final.pivot_table(values="value", index="year", columns="Parameteric", fill_value=0)
#Replace 0 values with Nan so that the don't appear in the graphs
pivot_Ireland_EachParametricOverTime.replace(0,np.nan, inplace=True)
#Convert to Dataframe
pivot_Ireland_EachParametricOverTime =pd.DataFrame(pivot_Ireland_EachParametricOverTime)
#Add in a new calculated column that contains the total number of hospital beds
pivot_Ireland_EachParametricOverTime['Total Hospital Beds'] = (pivot_Ireland_EachParametricOverTime['Hospital Beds per 1,000 people']/1000* pivot_Ireland_EachParametricOverTime['Total Population']).round(0)
pivot_Ireland_EachParametricOverTime.to_csv('EachParametricOverTime.csv')
#print(pivot_Ireland_EachParametricOverTime.head())

#Get summary page of number missing values for each indicator
Missing_values_by_parameter=pivot_Ireland_EachParametricOverTime.isna().sum()
#plot the number of missing values for each parameter
Missing_values_by_parameter.plot(kind = 'bar')
plt.xlabel("X Parameters")
plt.ylabel("Number Missind Data Points")

#Get the list of unique Parametric names that wil be used in the for loop that creates the subplot grid
parameters=Ireland_1990_final["Parameteric"].unique()
#set initial values for row and column index
r=0
c=0
#Plot parameters over time (years)
fig1, ax1 = plt.subplots(4, 4,figsize=(15, 10), facecolor='lightblue')
for param in parameters:
    row_df = Ireland_1990_final[Ireland_1990_final["Parameteric"]== param]
    ax1[r,c].plot(row_df['year'],row_df['value'], marker ='o', linestyle = '--')
    ax1[r,c].tick_params(axis='x', labelrotation = 45)
    ax1[3,c].set_xlabel('Time (years)')
    ax1[r,c].set_title(param)
    c += 1
    if c == 4:
        c = 0
        r += 1

#set initial values for row and column index
r=0
c=0
#Plot parameters against GNI per capita
fig2, ax2 = plt.subplots(4, 4,figsize=(15, 10), sharex='col',  facecolor='lightgreen')
for param in parameters:
    ax2[r, c].scatter(pivot_Ireland_EachParametricOverTime['GNI per capita'],pivot_Ireland_EachParametricOverTime[param], marker ='o', linestyle = '--')
    ax2[r, c].tick_params(axis='x', labelrotation=45)
    ax2[3, c].set_xlabel('GNI per Capita')
    ax2[r, c].set_title(param)
    c += 1
    if c == 4:
        c = 0
        r += 1

#User Defined Function puts two parameters onto the same time series plot with each getting it's own Y axes.
# input variable description in order ( x-axis parameter, x-axis label, Right Y axis parameter, Right Y axis label, Left Y axis parameter, Left Y axis label,
#                                          Right Y axis colour, Left Y axis colour, Linewidth of lines in graph)
def twin_plot(x, xlabel, y1,label_y1, y2, label_y2, color_y1, color_y2, linewidth):
    fig, ax = plt.subplots()
    ax.plot(x,y1, color=color_y1,linewidth=linewidth, marker ='o', markersize=4)
    ax.set_xlabel(xlabel)
    ax.set_facecolor('#eafff5')
    plt.xticks(np.arange(min(x), max(x) + 1, 1.0),rotation=90)
    ax.set_ylabel(label_y1, color=color_y1)
    ax.tick_params('y', colors=color_y1 )
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.vlines(2008, 0, 1, transform=ax.get_xaxis_transform(), colors='black',linewidth = linewidth, linestyles='dashdot', label='2008')
    ax2 = ax.twinx()
    ax2.plot(x, y2, color=color_y2, linewidth=linewidth,marker ='s', markersize=4)
    ax2.set_ylabel(label_y2, color=color_y2)
    ax2.tick_params('y', colors=color_y2)

#Here is where I explore the data in more detail with the user fucnction. Selcting metrics based on the plots created above.
#Hospital Beds per 1000 with GNP over time
twin_plot(pivot_Ireland_EachParametricOverTime.index,'Time(years)', pivot_Ireland_EachParametricOverTime['GNI per capita'],'GNP ($)',
          pivot_Ireland_EachParametricOverTime['Hospital Beds per 1,000 people'],'Hospital Beds per 1,000 people','red','blue',1)
#Total Hospital Beds with GNP over time
twin_plot(pivot_Ireland_EachParametricOverTime.index,'Time(years)', pivot_Ireland_EachParametricOverTime['GNI per capita'],'GNP ($)',
          pivot_Ireland_EachParametricOverTime['Total Hospital Beds'],'Total Hospital Beds','red','orange',1)
#% Unemployment with Total Tax Revenue over time
twin_plot(pivot_Ireland_EachParametricOverTime.index,'Time(years)', pivot_Ireland_EachParametricOverTime['Unemployment as % of Work Force'],'% Unemployment',
          pivot_Ireland_EachParametricOverTime['Total Tax revenue'],'Total Tax Revenue (LCU x 10Billion)','darkgreen','orange',1)
#Total Population with Life Expectancy over time
twin_plot(pivot_Ireland_EachParametricOverTime.index,'Time(years)', pivot_Ireland_EachParametricOverTime['Total Population'],'Total Population (millions)',
          pivot_Ireland_EachParametricOverTime['Life Expectancy at Birth'],'Life Expectancy at Birth (years)','teal','salmon',1)
#Number of Tourist departures with Greenhouse Gas (kt of CO2 equiv)
twin_plot(pivot_Ireland_EachParametricOverTime.index,'Time(years)', pivot_Ireland_EachParametricOverTime['Number Tourist Departures'],'Number Tourist Departures (millions)',
          pivot_Ireland_EachParametricOverTime['Greenhouse Gas (kt of CO2 equiv)'],'Greenhouse Gas (kilotonne of CO2 equiv)','sienna','violet',1)

plt.show()
