import pandas as pd

csv_dir = r'E://Tableau//records_4//frequency//agents_1_Numberwin503.csv'

df = pd.read_csv(csv_dir)
safe = []
banned = []

length = len(df)

for i in range(length-1):
    if(df.loc[i]['ip_time'] <= 2525):
        if(df.loc[i]['ip_time'] == df.loc[i]['time']):    continue
        else:
            if(df.loc[i]['ip_status'] == 2 and df.loc[i]['ip_status'] == df.loc[i+1]['ip_status'] ):
                banned.append(df.loc[i]['ip_time'])
            if(df.loc[i]['ip_status'] == 0):
                safe.append(df.loc[i]['ip_time'])

print('次数窗口')
print(len(safe))
print(len(banned))
print(len(banned) / (len(safe)+len(banned)))


safe = []
banned = []

length = len(df)

for i in range(length-1):
    if(df.loc[i]['ip_time'] <= 2525):
        if(df.loc[i]['ip_time'] == df.loc[i]['time']):    continue
        else:
            if(df.loc[i]['ip_status'] == 2 and df.loc[i]['ip_status'] == df.loc[i+1]['ip_status'] ):
                banned.append(df.loc[i]['ip_time'])
            if(df.loc[i]['ip_status'] == 0):
                safe.append(df.loc[i]['ip_time'])

print('时间窗口')
print(len(safe))
print(len(banned))
print(len(banned) / (len(safe)+len(banned)))