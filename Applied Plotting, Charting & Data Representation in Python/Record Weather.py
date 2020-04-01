import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
from datetime import datetime

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')




get_ipython().magic('matplotlib notebook')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

hashid = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89'

#load user specific data
data = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/{}.csv'.format(hashid))

#sort data by date
data = data.sort_values(by='Date')





#isolate 2015 data
data2015 = data[data['Date'].str.startswith('2015')]

#generalize 2015 data
data2015['Date'] = data2015['Date'].apply(lambda x: x[5:])
# print(data2015.head())



# #generalize all available date data
data['Date'] = data['Date'].apply(lambda x: x[5:])

# skip leap days
data = data[data['Date'] != '02-29']




record_overall_high = data.groupby('Date')['Data_Value'].max()
# print(record_overall_high.head())

record_overall_low = data.groupby('Date')['Data_Value'].min()
# print(record_overall_low.head())


high2015  = data2015.groupby('Date')['Data_Value'].max()
# print(high2015)

low2015 = data2015.groupby('Date')['Data_Value'].min()
# print(low2015.head())




record_high2015 = high2015[high2015 >= record_overall_high.reindex_like(high2015)]
# print(record_high2015.head())

record_low2015 = low2015[low2015 <= record_overall_low.reindex_like(low2015)]
# print(record_low2015.head())


x = np.linspace(1,365,365)
y = np.linspace(1,365,365)

#determine days when temperatures were unusually high/low
x = [n for n in range(0,365) if (high2015.iloc[n] >= record_overall_high.iloc[n]) ]
# print(x)


y = [n for n in range(0,365) if (low2015.iloc[n] <= record_overall_low.iloc[n]) ]
# print(y)



observation_dates = list(range(1,366))


plt.figure(figsize=(12,10))
ax1 = plt.gca()

ax1.set_xlabel('Day of the year')
ax1.set_ylabel('Temperature (tenths of degrees C)')
ax1.set_title('Record highest and lowest temperature by day of the year')

plt.plot(observation_dates,record_overall_high,'-',observation_dates,record_overall_low,'-',zorder=1)
ax1.legend(['record high temperatures', 'record low temperatures'])

plt.scatter(x,record_high2015,s=20,c='red',zorder=2,alpha=0.7)
plt.scatter(y,record_low2015,s=20,c='red',zorder=2,alpha=0.7)

ax1.legend(['record high temperatures', 'record low temperatures','record broken in 2015'])

ax1.fill_between(observation_dates,record_overall_high, record_overall_low, facecolor='blue', alpha=0.25)

# for spine in plt.gca().spines.values():
#     spine.set_visible(False)

plt.show()