import pandas as pd
import numpy as np
import os
import json
import datetime

from ploter import ploter

def prepare_csv(path):
    source_dic = {'idx':[],'time':[],'ip':[],'account':[],'status':[],'request_type':[],'request_status':[]}
    with open(path,'r') as f:
        list_data = json.load(f)
    for idx in range(len(list_data)):
        row = list_data[idx]
        source_dic['idx'].append(idx)
        source_dic['time'].append(row['time'])
        source_dic['ip'].append(row['ip'])
        source_dic['account'].append(row['account'])
        source_dic['status'].append(row['status']['code'])
        source_dic['request_type'].append(row['execution_detail']['request_type'].split(r'.')[-1])
        source_dic['request_status'].append(row['execution_detail']['is_success'])

    # request_set = set(source_dic['request_type'])
    # print(source_dic['request_type'])
    # print(request_set)
    source_csv = pd.DataFrame(source_dic)
    # print(source_csv.head())
    return source_csv

if __name__ == "__main__":
    json_dir = r'E://Tableau//records_1//agents_2.json'
    # json_dir = r'E://records_2//agents_1.json'
    csv_dir = r'E://Tableau//records_1//agents_2_TimeWin3000.csv'

    source_csv = prepare_csv(json_dir)
    
    """ print(source_csv.head())
    quit() """
    target_ip = list(set(list(source_csv['ip']))) 
    target_account = list(set(list(source_csv['account']))) 
    # target_ip = ['225.168.9.52', \
    #     '225.168.2.5', \
    #         '19.168.89.5', \
    #             '195.221.22.21', \
    #                 '192.168.1.5', \
    #                     '225.168.6.8', \
    #                         '195.221.68.34', \
    #                             '195.221.56.8', \
    #                                 '229.21.36.85']

    # print(datetime.datetime.now())
    # feature_ploter_by_time = ploter(target_ip=target_ip, target_account=target_account, t_start=0, t_stop=432000, \
    #     frequency = True, online_time = False, interval = False, type_name = 'Time', target_name = 'ip',\
    #         fre_ip_Twin = 3000, fre_ip_Nwin = 500, \
    #             fre_account_Twin = 3000, fre_account_Nwin = 600, \
    #                 online_ip_T = 86400, online_account_T = 86400,\
    #                     interval_ip_Twin = 3000, interval_ip_Nwin = 300, \
    #                         interval_account_Twin = 3000, interval_account_Nwin = 300)
    # dataset_by_number = feature_ploter_by_time.get_features(source_csv)
    # dataset_by_number.to_csv(csv_dir)
    
    print(datetime.datetime.now())

    feature_ploter_by_time = ploter(target_ip=target_ip, target_account=target_account, t_start=0, t_stop=432000, \
        frequency = True, online_time = False, interval = False, type_name = 'Time', target_name = 'ip',\
            fre_ip_Twin = 3000, fre_ip_Nwin = 600, \
                fre_account_Twin = 3000, fre_account_Nwin = 600, \
                    online_ip_T = 86400, online_account_T = 86400,\
                        interval_ip_Twin = 3000, interval_ip_Nwin = 500, \
                            interval_account_Twin = 3000, interval_account_Nwin = 500)
    dataset_by_time = feature_ploter_by_time.get_features(source_csv)
    print(datetime.datetime.now())
    dataset_by_time.to_csv(csv_dir)
            
    # dataset_by_time.to_csv('./time.csv',index=False)
    # dataset_by_number.to_csv('./number.csv',index=False)
