import pandas as pd
import glob
import datetime
import functions as fn
import argparse


parser = argparse.ArgumentParser(description="Plot mean temperature and NO2 values by month.")
parser.add_argument("-year", type=int, help="Specify the year for data filtering")
parser.add_argument("-path", help="Specify path of the folder with the data files")
args = parser.parse_args()
year=args.year
pathFiles=args.path
if year==2018:
    # Read the temperature dataframe
    pathTemp="./Anio201810/TemperaturaMeteoro/madrid_hourly_temperatures_2018.csv"
    dfTemp = pd.read_csv(pathTemp, sep=',', names=['date', 'hour', 'temp'], dtype={'date': str, 'hour': int, 'temp': float},header=1, parse_dates=True, decimal='.')

    dfTemp['date'] = pd.to_datetime(dfTemp['date'], format='%Y-%m-%d')
    dfTemp['hour'] = dfTemp['hour'].astype(int)

# Reading and transforming the contamination df
#pathFiles="./Anio201810"
files=glob.glob(pathFiles+"/*.csv")
listOfMonths=[]
for file in files:
    datos2018=pd.read_csv(file,sep=";")
    # Filter the data to only include the rows with MAGNITUD=8 beacuse it is the one that contains the NO2 values
    datos2018=datos2018.loc[datos2018["MAGNITUD"]==8]
    # create the date varible the same format as the one in the temperature dataframe
    datos2018["date"]=pd.to_datetime(dict(year=datos2018.ANO, month=datos2018.MES, day=datos2018.DIA))
    datos2018["date"] = datos2018["date"].dt.strftime('%Y-%m-%d')
    datos2018.drop(columns=["ANO","MES","DIA"],inplace=True)
    # create the variable punto_muestreo to macth with the queality stations
    datos2018["station"]=datos2018["PUNTO_MUESTREO"].str.split("_").str[0]
    # Drop the columns that are not needed
    datos2018.drop(columns=["PUNTO_MUESTREO"],inplace=True)
    
    # Create an ungruped dataframe with rows representing each hour of the day
    columnsVH= [col for col in datos2018.columns if col.startswith('V') or col.startswith('H')]
    pairDict = {}
    
    # Iterate over columns and group them by the last two digits
    for col in columnsVH:
        last2 = col[-2:]
        if last2 not in pairDict:
            pairDict[last2] = []
        pairDict[last2].append(col)

    # Concatenate columns with the same last two digits H01/V01, H02/V02, etc
    for key, value in pairDict.items():
        datos2018["hour"+key] = datos2018[value[0]].astype(str) + '/' +datos2018[value[1]].astype(str)
        datos2018.drop(columns=value,inplace=True)
    # Columns to melt the dataframe
    columnsHour= [col for col in datos2018.columns if col.startswith('hour')]
    columnsNotHour = [col for col in datos2018.columns if not col.startswith('hour')]

    # Melt the dataframe to have a row for each hour of the day
    datos2018_melt=pd.melt(datos2018,id_vars=columnsNotHour,value_vars=columnsHour,var_name="hour",value_name="H/V")
    # Create the H value and V value
    datos2018_melt[['H', 'V']] = datos2018_melt['H/V'].str.split('/', expand=True)
    datos2018_melt.drop(columns="H/V",inplace=True)
    # Extract the word hour from the variable hour and convert it to int so the variable shows the hour of the day
    datos2018_melt["hour"]=datos2018_melt["hour"].str.replace("hour","")
    datos2018_melt["hour"]=datos2018_melt["hour"].astype(int)
    # Assuming df is your DataFrame and columns_to_check is a list of columns to use as keys
    columns_to_check = ['PROVINCIA', 'MUNICIPIO', 'MAGNITUD', 'ESTACION', 'station', 'date', 'hour']

    # Remove duplicates if there are duplicates raise a warning
    datos2018_melt = fn.delete_duplicates(datos2018_melt, columns_to_check)

    # Concatenate this df with the previous df of the for loop
    listOfMonths.append(datos2018_melt)
    
    # Save the Dataframe to a csv file and name it with the month as number( easier to sort the files later on)
    months = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
    month=file.split("/")[-1].split("\\")[-1].split("_")[0]
    nameFile=f"./DataBase/{year}/{months[month]}_{month}.csv"

    # Convert the date to datetime format to merge it with the temperature dataframe
    datos2018_melt["date"] = pd.to_datetime(datos2018_melt["date"],format='%Y-%m-%d')
    if year==2018: 
        datos2018_merge=pd.merge(datos2018_melt,dfTemp,how="left",on=["date","hour"])
        datos2018_merge.to_csv(nameFile, index=False, decimal=".",sep=';')
    else:
        datos2018_melt.to_csv(nameFile, index=False, decimal=".",sep=';')

# Concatenate all the dataframes of the list
datos2018=pd.concat(listOfMonths, ignore_index=True)
datos2018["date"] = pd.to_datetime(datos2018["date"],format='%Y-%m-%d') 
datos2018["hour"] = datos2018["hour"].astype(int)
if year==2018:
    datos2018.to_csv(f"./DataBase/{year}/All_Months_NO2_{year}.csv", index=False, decimal=".",sep=';')
    # Save the Dataframe with Temperature to a csv file
    datos2018_merge=pd.merge(datos2018,dfTemp,how="left",on=["date","hour"])
    datos2018_merge.to_csv("./DataBase/2018/All_Months_NO2_Temp2018.csv", index=False, decimal=".",sep=';')
else:
    datos2018.to_csv(f"./DataBase/{year}/All_Months_NO2_{year}.csv", index=False, decimal=".",sep=';')