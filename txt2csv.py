import pandas as pd
import datetime

df = pd.read_csv(r'D:\GitHub\H2OGeomatics\climo\test data\Eg\air-temperature.txt', header = None, names =['Year','Month','Day','AirTemp'], delim_whitespace=True)
df['Cloud'] = pd.read_csv(r'D:\GitHub\H2OGeomatics\climo\test data\Eg\cloud-cover.txt', header = None, usecols = [3], delim_whitespace=True)
df['RelHum'] = pd.read_csv(r'D:\GitHub\H2OGeomatics\climo\test data\Eg\relative-humidity.txt', header = None, usecols = [3], delim_whitespace=True)
df['SnowFall'] = pd.read_csv(r'D:\GitHub\H2OGeomatics\climo\test data\Eg\snow-accumulation-rate.txt', header = None, usecols = [3], delim_whitespace=True)
df['WindSpd'] = pd.read_csv(r'D:\GitHub\H2OGeomatics\climo\test data\Eg\wind-speed.txt', header = None, usecols = [3], delim_whitespace=True)
df.insert(loc = 0, column='Date', value = pd.to_datetime(df[['Year', 'Month', 'Day']]))#.dt.strftime('%m/%d/%Y'))
df.drop(['Year','Month','Day'], axis=1, inplace=True)

df.to_csv(r'D:\GitHub\H2OGeomatics\climo_V2\test_data2.csv', index = None)


