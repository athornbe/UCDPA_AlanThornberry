
#Ireland_pivot_merge= Ireland_1990_pivot1.merge(Ireland_1990_pivot3, on="series_id")
#Ireland_pivot_merge.to_csv("D:\My Documents\Downloads\Ireland_pivot_merge.csv")

Ireland_GDP= Ireland_1990_final[Ireland_1990_final["series_id"]=="SL.GDP.PCAP.EM.KD"]
Ireland_GDP.to_csv("Ireland_GDP.csv")
Ireland_GNP= Ireland_1990_final[Ireland_1990_final["series_id"]=="NY.GNP.PCAP.PP.CD"]
Ireland_GNP.to_csv("D:\My Documents\Downloads\Ireland_GNP.csv")


Ireland_GDP_pivot = Ireland_GDP.pivot_table(values="value", index="year", columns="series_id", fill_value=0)
Ireland_GDP_pivot.to_csv("D:\My Documents\Downloads\Ireland_GDP_pivot.csv")
#print(Ireland_GDP_pivot.info)

#GDP over time
fig, ax= plt.subplots()
ax.plot(Ireland_GDP["year"],Ireland_GDP["value"], marker ='o', linestyle = '--')
ax.grid(b=True, which='major', axis='both')
plt.xticks(np.arange(min(Ireland_GDP["year"]), max(Ireland_GDP["year"])+1, 1.0), rotation= 90)
plt.yticks(np.arange(min(Ireland_GDP["value"]), max(Ireland_GDP["value"])+1, 5000.0))
ax.set_xlabel('Time (years)')
ax.set_ylabel('GDP per person employed')

#GNP over time
fig1, ax= plt.subplots()
ax.plot(Ireland_GNP["year"],Ireland_GNP["value"], marker ='o', linestyle = '--')
ax.grid(b=True, which='major', axis='both')
plt.xticks(np.arange(min(Ireland_GNP["year"]), max(Ireland_GNP["year"])+1, 1.0), rotation= 90)
plt.yticks(np.arange(min(Ireland_GNP["value"]), max(Ireland_GNP["value"])+1, 5000.0))
ax.set_xlabel('Time (years)')
ax.set_ylabel('GNI per person employed')
plt.show()


#Sample Graph with multiple y(output) variables
price_diffs.plot(y=['close_jpm','close_wells','close_bac'])
#Same result
price_diffs.plot(kind='line',x='date_time',y=['close_jpm','close_wells','close_bac'])
#another sample
gdp_recession.plot(kind='bar', y='gdp', x='date', rot=90)
plt.show()


Ireland_GDP_pivot.plot(kind='scatter', x='year', y='SL.GDP.PCAP.EM.KD')
plt.show()
sns.scatterplot(x=Ireland_GDP["year"], y=Ireland_GDP["value"])
plt.show()

sns.scatterplot(x=Ireland_GDP_pivot["year"], y=Ireland_GDP_pivot["SL.GDP.PCAP.EM.KD"])
plt.show()



#g = sns.PairGrid(pivot_Ireland_EachParametricOverTime)
#g.map_diag(sns.histplot)
#g.map_offdiag(sns.scatterplot)
#plt.show()

#sns.PairGrid(pivot_Ireland_EachParametricOverTime, y_vars="GNI per capital", x_vars=pivot_Ireland_EachParametricOverTime.columns.values)
#plt.show()

col = 'GNI per capital'
df2 = pivot_Ireland_EachParametricOverTime.drop(col,axis=1)
df2.index = pivot_Ireland_EachParametricOverTime[col]
df2.plot(subplots=True, style='.')
plt.legend(loc='best')
plt.show()