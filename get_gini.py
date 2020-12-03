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
    json_dir = r'E://Tableau//records_1//agents_4.json'
    # json_dir = r'E://records_2//agents_1.json'
    csv_dir = r'E://Tableau//records_1//frequency//agents_1_Timewin1000-new----test.csv'

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
    # search_dic_number = {}
    # # upper_bound = source_csv[source_csv['status'] == 4]['time'].min()
    # print(datetime.datetime.now())
    # for number_window in range(20, 501, 20):
    #     feature_ploter_by_time = ploter(target_ip=target_ip, target_account=target_account, t_start=0, t_stop=432000, \
    #         frequency = False, online_time = False, interval = True, type_name = 'Number', target_name = 'ip',\
    #             fre_ip_Twin = 3000, fre_ip_Nwin = number_window, \
    #                 fre_account_Twin = 3000, fre_account_Nwin = 600, \
    #                     online_ip_T = 86400, online_account_T = 86400,\
    #                         interval_ip_Twin = 3000, interval_ip_Nwin = number_window, \
    #                             interval_account_Twin = 3000, interval_account_Nwin = 500)
    #     dataset = feature_ploter_by_time.get_features(source_csv)
    #     line_location = {}
    #     # line_location['std'] = dataset[dataset['ip_status'] == 2]['ip_interval_std'].max()
    #     # line_location['max-mean'] = dataset[dataset['ip_status'] == 2]['ip_interval_max-mean'].max()
    #     line_location['min-mean'] = dataset[dataset['ip_status'] == 2]['ip_interval_min-mean'].max()
    #     search_dic_number[number_window] = feature_ploter_by_time.get_gini(dataset, line_location)
    # print('search_dic_number: {}'.format(search_dic_number))
    # print(datetime.datetime.now())
            
    # number_gini_ip_interval_std = {}
    # number_gini_ip_interval_max_mean = {}
    # number_gini_ip_interval_min_mean = {}
    # for i in search_dic_number.keys():
    #     number_gini_ip_interval_std[i] = search_dic_number[i]['ip_interval']['std']
    #     number_gini_ip_interval_max_mean[i] = search_dic_number[i]['ip_interval']['max-mean']
    #     number_gini_ip_interval_min_mean[i] = search_dic_number[i]['ip_interval']['min-mean']
    # numberW_gini_std = pd.DataFrame(number_gini_ip_interval_std,index = [0])
    # numberW_gini_max_mean = pd.DataFrame(number_gini_ip_interval_max_mean,index = [0])
    # numberW_gini_min_mean = pd.DataFrame(number_gini_ip_interval_min_mean,index = [0])
    # numberW_gini_std.to_csv('./gini/interval/numberW_gini_std.csv', index=False)
    # numberW_gini_max_mean.to_csv('./gini/interval/numberW_gini_max-mean.csv', index=False)
    # numberW_gini_min_mean.to_csv('./gini/interval/numberW_gini_min-mean.csv', index=False)

    search_dic_time = {}
    # upper_bound = source_csv[source_csv['status'] == 4]['time'].min()
    print(datetime.datetime.now())
    for time_window in range(2000, 4550, 100):
        feature_ploter_by_time = ploter(target_ip=target_ip, target_account=target_account, t_start=0, t_stop=432000, \
            frequency = False, online_time = False, interval = True, type_name = 'Time', target_name = 'ip',\
                fre_ip_Twin = time_window, fre_ip_Nwin = 600, \
                    fre_account_Twin = 3000, fre_account_Nwin = 600, \
                        online_ip_T = 86400, online_account_T = 86400,\
                            interval_ip_Twin = time_window, interval_ip_Nwin = 500, \
                                interval_account_Twin = 3000, interval_account_Nwin = 500)
        dataset = feature_ploter_by_time.get_features(source_csv)
        line_location = {}
        line_location['std'] = dataset[dataset['ip_status'] == 2]['ip_interval_std'].max()
        line_location['max-mean'] = dataset[dataset['ip_status'] == 2]['ip_interval_max-mean'].max()
        line_location['min-mean'] = dataset[dataset['ip_status'] == 2]['ip_interval_min-mean'].max()
        search_dic_time[time_window] = feature_ploter_by_time.get_gini(dataset, line_location)
    print('search_dic_time: {}'.format(search_dic_time))
    print(datetime.datetime.now())

    time_gini_ip_interval_std = {}
    time_gini_ip_interval_max_mean = {}
    time_gini_ip_interval_min_mean = {}
    for i in search_dic_time.keys():
        time_gini_ip_interval_std[i] = search_dic_time[i]['ip_interval']['std']
        time_gini_ip_interval_max_mean[i] = search_dic_time[i]['ip_interval']['max-mean']
        time_gini_ip_interval_min_mean[i] = search_dic_time[i]['ip_interval']['min-mean']
    timeW_gini_std = pd.DataFrame(time_gini_ip_interval_std,index = [0])
    timeW_gini_max_mean = pd.DataFrame(time_gini_ip_interval_max_mean,index = [0])
    timeW_gini_min_mean = pd.DataFrame(time_gini_ip_interval_min_mean,index = [0])
    timeW_gini_std.to_csv('./gini/interval/timeW_gini_std.csv', index=False)
    timeW_gini_max_mean.to_csv('./gini/interval/timeW_gini_max-mean.csv', index=False)
    timeW_gini_min_mean.to_csv('./gini/interval/timeW_gini_min-mean.csv', index=False)
    
