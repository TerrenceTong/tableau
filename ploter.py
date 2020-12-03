import pandas as pd
import datetime as dt
import numpy as np


class ploter():
    def __init__(self, target_ip=[], target_account=[], t_start=0, t_stop=432000, \
        frequency = True, online_time = True, interval = True, type_name = 'Number', target_name = 'ip' ,\
            fre_ip_Twin = 3000, fre_ip_Nwin = 500, \
                fre_account_Twin = 3000, fre_account_Nwin = 500, \
                    online_ip_T = 86400, online_account_T = 86400,\
                        interval_ip_Twin = 3000, interval_ip_Nwin = 500, \
                            interval_account_Twin = 3000, interval_account_Nwin = 500):
        self.target_ip = target_ip
        self.target_account = target_account
        self.t_start = t_start
        self.t_stop = t_stop
        self.frequency = frequency
        self.online_time = online_time
        self.interval = interval
        self.type_name = type_name
        self.target_name = target_name
        self.fre_ip_Twin = fre_ip_Twin
        self.fre_ip_Nwin = fre_ip_Nwin
        self.fre_account_Twin = fre_account_Twin
        self.fre_account_Nwin = fre_account_Nwin
        self.online_ip_T = online_ip_T
        self.online_ip_account_T = online_account_T
        self.interval_ip_Twin = interval_ip_Twin
        self.interval_ip_Nwin = interval_ip_Nwin
        self.interval_account_Twin = interval_account_Twin
        self.interval_account_Nwin = interval_account_Nwin
    # ip特征-时间窗口
    def get_ip_features_by_timeW(self, data, ip_time, ip_status, dataset):
        for i in ip_time.keys():
            if(i not in self.target_ip): continue
            print(i)
            ip_total = 0
            ip_online_start = ip_time[i][0][1]

            for j in range(len(ip_time[i])):
                idx = ip_time[i][j][0]
                # print(idx)
                time = ip_time[i][j][1]
                if(time < self.t_start or time > self.t_stop):    continue
                if(ip_status[i][j][1] == 4 and ip_status[i][j][1] == ip_status[i][j-1][1]): continue

                pre_timestamp_num = j
                if(self.frequency):
                    # 计算频率
                    # if(ip_status[i][j][1] == 4 and ip_status[i][j][1] == ip_status[i][j-1][1]):
                    #     fre_feature = None
                    # else:
                    while(pre_timestamp_num > 0 and \
                        time - ip_time[i][pre_timestamp_num][1] < self.fre_ip_Twin):
                        pre_timestamp_num -= 1
                    if(time - ip_time[i][pre_timestamp_num][1] < self.fre_ip_Twin):
                        fre_feature = None
                    else:
                        fre_feature = j - pre_timestamp_num
                if(self.interval):
                    # 计算间隔
                    pre_timestamp_interval = j
                    interval_record = []
                    while(pre_timestamp_interval > 0 and \
                        time - ip_time[i][pre_timestamp_interval][1] < self.interval_ip_Twin):
                        pre_timestamp_interval -= 1
                        # print(i, j)
                        # print(ip_time[i][pre_timestamp_interval+1][1])
                        # print(ip_time[i][pre_timestamp_interval][1])
                        interval_record.append((ip_time[i][pre_timestamp_interval+1][1]) - \
                            (ip_time[i][pre_timestamp_interval][1]))
                        # print(interval_record)
                    if(time - ip_time[i][pre_timestamp_interval][1] < self.interval_ip_Twin):
                        interval_record = []

                    # # 计算间隔
                    # pre_timestamp_interval = j
                    # interval_record = []
                    # while(pre_timestamp_interval > 0 and \
                    #     time - ip_time[i][pre_timestamp_interval][1] < self.interval_ip_Twin):
                    #     pre_timestamp_interval -= 1
                    #     interval_record.append(time - ip_time[i][pre_timestamp_interval][1])

                if(self.online_time):
                    # 计算在线时长
                    ip_online = ip_time[i][j][1] - ip_online_start
                    if(j < len(ip_time[i])-1 and ip_time[i][j+1][1] - ip_time[i][j][1] > self.online_ip_T):
                        ip_online_start = ip_time[i][j+1][1]

                    pre_pre_timestamp_online = j - 1
                    pre_timestamp_online = j
                    while(pre_pre_timestamp_online > 0 and ip_time[i][pre_timestamp_online][1] - ip_time[i][pre_pre_timestamp_online][1] < self.online_ip_T):
                        pre_pre_timestamp_online -= 1
                        pre_timestamp_online -= 1
                    ip_online = time - ip_time[i][pre_timestamp_online][1]
                    
                if(idx not in dataset.index):
                    print('wrong idx!')
                    quit()
                if(ip_status[i][j][1] == 0 or ip_status[i][j][1]==1 or ip_status[i][j][1]==2):
                    dataset.loc[idx]['ip_status'] = 0
                if(ip_status[i][j][1] == 3):
                    dataset.loc[idx]['ip_status'] = 1
                if(ip_status[i][j][1] == 4):
                    dataset.loc[idx]['ip_status'] = 2
                    
                dataset.loc[idx]['ip'] = i
                dataset.loc[idx]['time'] = time
                if(self.frequency):
                    dataset.loc[idx]['ip_num'] = fre_feature
                    # dataset.loc[idx]['ip_num'] = j+1
                if(self.interval):
                    if(len(interval_record) < 2):   dataset.loc[idx]['ip_interval'] = 0
                    else:   
                        max_ = np.max(interval_record)
                        mean_ = np.mean(interval_record)
                        min_ = np.min(interval_record)
                        record = 0.0
                        record_2 = 0.0
                        if(max_ - mean_ > mean_ - min_):    
                            record = max_ - mean_
                            record_2 = mean_ - min_
                        else:   
                            record = mean_ - min_
                            record_2 = max_ - mean_
                        dataset.loc[idx]['ip_interval_std'] = np.std(interval_record)
                        dataset.loc[idx]['ip_interval_max-mean'] = record
                        dataset.loc[idx]['ip_interval_min-mean'] = record_2
                        dataset.loc[idx]['ip_interval_var'] = np.var(interval_record)
                        dataset.loc[idx]['ip_mean'] = np.mean(interval_record)
                if(self.online_time):
                    dataset.loc[idx]['ip_online'] = ip_online
                    # dataset.loc[idx]['ip_total'] = ip_total
    # account特征-时间窗口
    def get_account_features_by_timeW(self, data, account_time, account_status, dataset):
        for i in account_time.keys():
            if(i not in self.target_account): continue
            print(i)
            account_total = 0
            account_online_start = account_time[i][0][1]
            for j in range(len(account_time[i])):
                # print(idx)
                idx = account_time[i][j][0]
                time = account_time[i][j][1]
                if(time < self.t_start or time > self.t_stop):    continue
                if((account_status[i][j][1] == 2 or account_status[i][j][1] == 4) \
                    and account_status[i][j][1] == account_status[i][j-1][1]):
                    continue
                if(self.frequency):
                    # 计算频率
                    # if((account_status[i][j][1] == 2 or account_status[i][j][1] == 4) \
                    #     and account_status[i][j][1] == account_status[i][j-1][1]):
                    #     fre_feature = None
                    # else:
                    pre_timestamp_num = j
                    while(pre_timestamp_num > 0 and \
                        time - account_time[i][pre_timestamp_num][1] < self.fre_account_Twin):
                        pre_timestamp_num -= 1
                    if(time - account_time[i][pre_timestamp_num][1] < self.fre_account_Twin):
                        fre_feature = None
                    else:
                        fre_feature = j-pre_timestamp_num
                if(self.interval):
                    # 计算间隔
                    pre_timestamp_interval = j
                    interval_record = []
                    while(pre_timestamp_interval > 0 and \
                        time - account_time[i][pre_timestamp_interval][1] < self.interval_account_Twin):
                        pre_timestamp_interval -= 1
                        interval_record.append(time - account_time[i][pre_timestamp_interval][1])
                if(self.online_time):
                    # 计算在线时长
                    account_online = account_time[i][j][1] - account_online_start
                    if(j < len(account_time[i])-1 and account_time[i][j+1][1] - account_time[i][j][1] > self.online_account_T):
                        account_online_start = account_time[i][j+1][1]
                    # 计算在线时长
                        """ pre_pre_timestamp_online = j - 1
                        pre_timestamp_online = j
                        while(pre_pre_timestamp_online > 0 and \
                            account_time[i][pre_timestamp_online][1] - account_time[i][pre_pre_timestamp_online][1] \
                                < t1_account_online):
                            pre_pre_timestamp_online -= 1
                            pre_timestamp_online -= 1
                        account_online = time - account_time[i][pre_timestamp_online][1] """   

                if(idx not in dataset.index):
                    print('wrong indx!')
                    quit()
                    
                if(account_status[i][j][1] == 0):
                    dataset.loc[idx]['account_status'] = 0
                if(account_status[i][j][1] == 1 or account_status[i][j][1] == 3):
                    dataset.loc[idx]['account_status'] = 1
                if(account_status[i][j][1] == 2 or account_status[i][j][1] == 4):
                    dataset.loc[idx]['account_status'] = 2
                dataset.loc[idx]['account'] = i
                dataset.loc[idx]['time'] = time
                dataset.loc[idx]['status'] = account_status[i][j][1]
                if(self.frequency):
                    dataset.loc[idx]['account_num'] = fre_feature
                if(self.interval):
                    if(len(interval_record) < 2):  dataset.loc[idx]['account_interval'] = 0
                    else:
                        max_ = np.max(interval_record)
                        mean_ = np.mean(interval_record)
                        min_ = np.min(interval_record)
                        record = 0.0
                        record_2 = 0.0
                        if(max_ - mean_ > mean_ - min_):    
                            record = max_ - mean_
                            record_2 = mean_ - min_
                        else:   
                            record = mean_ - min_
                            record_2 = max_ - mean_
                        dataset.loc[idx]['account_interval_std'] = np.std(interval_record)
                        dataset.loc[idx]['account_interval_max-mean'] = record
                        dataset.loc[idx]['account_interval_min-mean'] = record_2
                        dataset.loc[idx]['account_interval_var'] = np.var(interval_record)
                        dataset.loc[idx]['account_mean'] = np.mean(interval_record)
                        
                if(self.online_time):
                    dataset.loc[idx]['account_online'] = account_online
                        # dataset.loc[idx]['account_total'] = account_total
    
    # ip特征-次数窗口
    def get_ip_features_by_numberW(self, data, ip_time, ip_status, dataset):
        for i in ip_time.keys():
            if(i not in self.target_ip): continue
            print(i)
            ip_total = 0
            ip_online_start = ip_time[i][0][1]
            for j in range(len(ip_time[i])):
                idx = ip_time[i][j][0]
                # print(idx)
                time = ip_time[i][j][1]
                if(time < self.t_start or time > self.t_stop):    continue
                if(ip_status[i][j][1] == 4 and ip_status[i][j][1] == ip_status[i][j-1][1]): continue

                pre_timestamp_num = j
                if(self.frequency):
                    # 计算频率
                    # if(ip_status[i][j][1] == 4 and ip_status[i][j][1] == ip_status[i][j-1][1]):
                    #     fre_feature = None
                    # else:
                    num = 0
                    while(pre_timestamp_num > 0 and \
                        num < self.fre_ip_Nwin):
                        num += 1
                        pre_timestamp_num -= 1
                    
                    if(num < self.fre_ip_Nwin):
                        fre_feature = None
                    else:
                        fre_feature = ip_time[i][j][1] - ip_time[i][pre_timestamp_num][1]
                if(self.interval):
                    # 计算间隔
                    num = 0
                    pre_timestamp_interval = j
                    interval_record = []
                    while(pre_timestamp_interval > 0 and \
                        num < self.interval_ip_Nwin):
                        num += 1
                        pre_timestamp_interval -= 1
                        # print(i, j)
                        # print(ip_time[i][pre_timestamp_interval+1][1])
                        # print(ip_time[i][pre_timestamp_interval][1])
                        interval_record.append((ip_time[i][pre_timestamp_interval+1][1]) - \
                            (ip_time[i][pre_timestamp_interval][1]))
                        # print(interval_record)
                    if(num < self.interval_ip_Nwin):    interval_record = []
                if(self.online_time):
                    # 计算在线时长
                    ip_online = ip_time[i][j][1] - ip_online_start
                    if(j < len(ip_time[i])-1 and ip_time[i][j+1][1] - ip_time[i][j][1] > self.online_ip_T):
                        ip_online_start = ip_time[i][j+1][1]
                
                # 保存dataset
                if(idx not in dataset.index):
                    print('wrong idx!')
                    quit()
                
                if(ip_status[i][j][1] == 0 or ip_status[i][j][1]==1 or ip_status[i][j][1]==2):
                    dataset.loc[idx]['ip_status'] = 0
                if(ip_status[i][j][1] == 3):
                    dataset.loc[idx]['ip_status'] = 1
                if(ip_status[i][j][1] == 4):
                    dataset.loc[idx]['ip_status'] = 2
                dataset.loc[idx]['ip'] = i
                dataset.loc[idx]['time'] = time
                if(self.frequency):
                    dataset.loc[idx]['ip_time'] = fre_feature
                if(self.interval):
                    if(len(interval_record) < 2):   
                        dataset.loc[idx]['ip_interval_std'] = None
                        dataset.loc[idx]['ip_interval_max-mean'] = None
                        dataset.loc[idx]['ip_interval_max-min'] = None
                    else:
                        # if(len(interval_record) == 10): quit()
                        max_ = np.max(interval_record)
                        mean_ = np.mean(interval_record)
                        min_ = np.min(interval_record)
                        record = 0.0
                        record_2 = 0.0
                        if(max_ - mean_ > mean_ - min_):    
                            record = max_ - mean_
                            record_2 = mean_ - min_
                        else:   
                            record = mean_ - min_
                            record_2 = max_ - mean_
                        dataset.loc[idx]['ip_interval_std'] = np.std(interval_record)
                        dataset.loc[idx]['ip_interval_max-mean'] = record
                        dataset.loc[idx]['ip_interval_min-mean'] = record_2
                        dataset.loc[idx]['ip_interval_var'] = np.var(interval_record)
                        dataset.loc[idx]['ip_mean'] = np.mean(interval_record)
                if(self.online_time):
                    dataset.loc[idx]['ip_online'] = ip_online
    # account-次数窗口
    def get_account_features_by_numberW(self, data, account_time, account_status, dataset):
        for i in account_time.keys():
            if(i not in self.target_account): continue
            print(i)
            account_total = 0
            account_online_start = account_time[i][0][1]
            """ print(account_online_start)
            quit() """
            for j in range(len(account_time[i])):
                idx = account_time[i][j][0]
                # print(idx)
                time = account_time[i][j][1]
                if(time < self.t_start or time > self.t_stop):    continue
                if((account_status[i][j][1] == 2 or account_status[i][j][1] == 4) \
                    and account_status[i][j][1] == account_status[i][j-1][1]):
                    continue
                pre_timestamp_num = j
                if(self.frequency):
                    # 计算频率
                    # if((account_status[i][j][1] == 2 or account_status[i][j][1] == 4) \
                    #     and account_status[i][j][1] == account_status[i][j-1][1]):
                    #     fre_feature = None
                    # else:
                    num = 0
                    while(pre_timestamp_num > 0 and \
                        num < self.fre_account_Nwin):
                        num += 1
                        pre_timestamp_num -= 1
                    if(num < self.fre_account_Nwin):
                        fre_feature = None
                    else:
                        fre_feature = account_time[i][j][1] - account_time[i][pre_timestamp_num][1]
                if(self.interval):
                    # 计算间隔
                    num = 0
                    pre_timestamp_interval = j
                    interval_record = []
                    while(pre_timestamp_interval > 0 and \
                        num < self.interval_account_Nwin):
                        num += 1
                        pre_timestamp_interval -= 1
                        # print(i, j)
                        # print(ip_time[i][pre_timestamp_interval+1][1])
                        # print(ip_time[i][pre_timestamp_interval][1])
                        interval_record.append((account_time[i][pre_timestamp_interval+1][1]) - \
                            (account_time[i][pre_timestamp_interval][1]))
                        # print(interval_record)
                    if(num < self.interval_account_Nwin):    interval_record = []
                if(self.online_time):
                    # 计算在线时长
                    account_online = account_time[i][j][1] - account_online_start
                    if(j < len(account_time[i])-1 and account_time[i][j+1][1] - account_time[i][j][1] > self.online_account_T):
                        account_online_start = account_time[i][j+1][1]
                
                # 保存dataset
                if(idx not in dataset.index):
                    print('wrong idx!')
                    quit()
                
                if(account_status[i][j][1] == 0 or account_status[i][j][1]==1 or account_status[i][j][1]==2):
                    dataset.loc[idx]['account_status'] = 0
                if(account_status[i][j][1] == 3):
                    dataset.loc[idx]['account_status'] = 1
                if(account_status[i][j][1] == 4):
                    dataset.loc[idx]['account_status'] = 2
                dataset.loc[idx]['account'] = i
                dataset.loc[idx]['time'] = time
                if(self.frequency):
                    dataset.loc[idx]['account_time'] = fre_feature
                if(self.interval):
                    if(len(interval_record) < 2):   
                        dataset.loc[idx]['account_interval_std'] = None
                        dataset.loc[idx]['account_interval_max-mean'] = None
                        dataset.loc[idx]['account_interval_max-min'] = None
                    else:
                        # if(len(interval_record) == 10): quit()
                        max_ = np.max(interval_record)
                        mean_ = np.mean(interval_record)
                        min_ = np.min(interval_record)
                        record = 0.0
                        record_2 = 0.0
                        if(max_ - mean_ > mean_ - min_):    
                            record = max_ - mean_
                            record_2 = mean_ - min_
                        else:   
                            record = mean_ - min_
                            record_2 = max_ - mean_
                        dataset.loc[idx]['account_interval_std'] = np.std(interval_record)
                        dataset.loc[idx]['account_interval_max-mean'] = record
                        dataset.loc[idx]['account_interval_min-mean'] = record_2
                        dataset.loc[idx]['account_interval_var'] = np.var(interval_record)
                        dataset.loc[idx]['account_mean'] = np.mean(interval_record)
                if(self.online_time):
                    dataset.loc[idx]['account_online'] = account_online

    def get_features_by_time(self, data, dataset):
        # data = source_csv
        ip_time = {}
        ip_status = {}
        account_time = {}
        account_status = {}
        for i, item in data.iterrows():
            t = item['time']
            ip = item['ip']
            account = item['account']
            status = item['status']
            idx = item['idx']
            if(ip in ip_time.keys()):
                ip_time[ip].append((idx, t))
                ip_status[ip].append((idx, status))
            else:
                ip_time[ip] = [(idx, t)]
                ip_status[ip] = [(idx, status)]
            if(account in account_time.keys()):
                account_time[account].append((idx, t))
                account_status[account].append((idx, status))
            else:
                account_time[account] = [(idx, t)]
                account_status[account] = [(idx, status)]
        if(self.target_name == 'ip'):
            self.get_ip_features_by_timeW(data, ip_time, ip_status, dataset)
        if(self.target_name == 'account'):
            self.get_account_features_by_timeW(data, account_time, account_status, dataset)
        if(self.target_name == 'all'):
            self.get_ip_features_by_timeW(data, ip_time, ip_status, dataset)
            self.get_account_features_by_timeW(data, account_time, account_status, dataset)

    def get_features_by_number(self, data, dataset):
        ip_time = {}
        ip_status = {}
        account_time = {}
        account_status = {}
        for i, item in data.iterrows():
            t = item['time']
            ip = item['ip']
            account = item['account']
            status = item['status']
            idx = item['idx']
            """ request_type = item['request_type']
            request_status = item['request_status'] """
            if(ip in ip_time.keys()):
                ip_time[ip].append((idx, t))
                ip_status[ip].append((idx, status))
            else:
                ip_time[ip] = [(idx, t)]
                ip_status[ip] = [(idx, status)]
            if(account in account_time.keys()):
                account_time[account].append((idx, t))
                account_status[account].append((idx, status))
            else:
                account_time[account] = [(idx, t)]
                account_status[account] = [(idx, status)]
        if(self.target_name == 'ip'):
            self.get_ip_features_by_numberW(data, ip_time, ip_status, dataset)
        if(self.target_name == 'account'):
            self.get_account_features_by_numberW(data, account_time, account_status, dataset)
        if(self.target_name == 'all'):
            self.get_ip_features_by_numberW(data, ip_time, ip_status, dataset)
            self.get_account_features_by_numberW(data, account_time, account_status, dataset)
        # return dataset

    def get_features(self, data):
        if(self.type_name == 'Time'):
            dataset = pd.DataFrame(columns=[ \
            'time', 'ip', 'account', \
                'ip_num', 'account_num', \
                    'ip_interval_std', 'ip_mean', 'ip_interval_var', 'ip_interval_max-mean', 'ip_interval_min-mean', \
                        'account_interval_std', 'account_mean', 'account_interval_var', 'account_interval_max-mean', 'account_interval_min-mean', \
                            'ip_online', 'account_online', \
                                'ip_status', \
                                    'account_status', \
                                        'status'], \
                                    index=data['idx'])
            self.get_features_by_time(data, dataset)
            return dataset
        if(self.type_name == 'Number'):
            dataset = pd.DataFrame(columns=[ \
            'time', 'ip', 'account', \
                'ip_time', 'account_time', \
                    'ip_interval_std','ip_mean', 'ip_interval_var', 'ip_interval_max-mean', 'ip_interval_min-mean', \
                        'account_interval_std','account_mean', 'account_interval_var', 'account_interval_max-mean', 'account_interval_min-mean', \
                            'ip_online', 'account_online', \
                                'ip_status', \
                                    'account_status', \
                                        'status'], \
                                    index=data['idx'])
            self.get_features_by_number(data, dataset)
            return dataset


    def get_ip_statistical(data):
        ip_sta = []
        ip_0_1 = {}
        ip_0_2 = {}
        ip_1_0 = {}
        ip_1_2 = {}
        ip_2_0 = {}
        # for i, item in data.iterrows():
        for name, group in data.groupby('ip'):
            if name.isnull(): continue
            else:
                group.reset_index(drop=True)
                for i in range(1, group.shape[0]) :
                    if(df.loc[i-1]['ip_status'] == 0 and df.loc[i]['ip_status'] == 1):
                        if(name in ip_0_1.keys()):
                            ip_0_1[name].append( (df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min']) )
                        else:
                            ip_0_1[name] = [(df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min'])]
                if(df.loc[i-1]['ip_status'] == 0 and df.loc[i]['ip_status'] == 2):
                        if(name in ip_0_2.keys()):
                            ip_0_2[name].append( (df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min']) )
                        else:
                            ip_0_2[name] = [(df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min'])]
                if(df.loc[i-1]['ip_status'] == 1 and df.loc[i]['ip_status'] == 0):
                        if(name in ip_1_0.keys()):
                            ip_1_0[name].append( (df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min']) )
                        else:
                            ip_1_0[name] = [(df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min'])]
                if(df.loc[i-1]['ip_status'] == 1 and df.loc[i]['ip_status'] == 2):
                        if(name in ip_1_2.keys()):
                            ip_1_2[name].append( (df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min']) )
                        else:
                            ip_1_2[name] = [(df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min'])]
                if(df.loc[i-1]['ip_status'] == 2 and df.loc[i]['ip_status'] == 0):
                        if(name in ip_2_0.keys()):
                            ip_2_0[name].append( (df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min']) )
                        else:
                            ip_2_0[name] = [(df.loc[i]['ip_num'], df.loc[i]['ip_online'], \
                                df.loc[i]['ip_interval_std'], df.loc[i]['ip_interval_max-mean'], \
                                    df.loc[i]['ip_interval_max-min'])]

        for ip in ip_0_1.keys():
            lst_fre = []
            lst_online = []
            lst_interval_std = []
            lst_interval_max_mean = []
            lst_interval_max_min = []
            for tu in ip_0_1[ip]:
                lst_fre.append(tu[0])
                lst_online.append(tu[1])
                lst_interval_std.append(tu[2])
                lst_interval_max_mean.append(tu[3])
                lst_interval_max_min.append(tu[4])
            ip_0_1[ip] = ()

        return 0
  

    def get_gini(self, dataset, line_location):
        gini_dic = {'ip_frequency':0.0, 'ip_online_time':0.0, 'ip_interval':{'std': 0.0, 'max-mean': 0.0, 'min-mean':0.0},\
            'account_frequency':0.0, 'account_online_time':0.0, 'account_interval':0.0}
        # dataset = self.get_features(data).dropna(subset=['ip_num'])
        if(self.type_name == 'Time'):
            if(self.frequency and self.target_name == 'ip'):
                dataset = dataset.dropna(subset=['ip_num'])
                df_up = dataset[dataset['ip_num'] > line_location - 1]
                df_up_count = df_up['ip_status'].groupby(df_up['ip_status']).count()
                # print(df_up_count)
                # print(df_up_count.index)
                prop = df_up_count.loc[2] / np.sum(df_up_count.values.tolist())
                gini_dic['ip_frequency'] = 2*prop - 2*prop*prop
                print('y = {}, gini = {}'.format(line_location, gini_dic['ip_frequency']))
            if(self.interval and self.target_name == 'ip'):
                dataset_std = dataset.dropna(subset=['ip_interval_std'])
                df_down_std = dataset[dataset['ip_interval_std'] < line_location['std'] + 1]
                df_down_count_std = df_down_std['ip_status'].groupby(df_down_std['ip_status']).count()
                prop = df_down_count_std.loc[2] / np.sum(df_down_count_std.values.tolist())
                gini_dic['ip_interval']['std'] = 2*prop - 2*prop*prop

                dataset_max_mean = dataset.dropna(subset=['ip_interval_max-mean'])
                df_down_max_mean = dataset[dataset['ip_interval_max-mean'] < line_location['max-mean'] + 1]
                df_down_count_max_mean = df_down_max_mean['ip_status'].groupby(df_down_max_mean['ip_status']).count()
                prop = df_down_count_max_mean.loc[2] / np.sum(df_down_count_max_mean.values.tolist())
                gini_dic['ip_interval']['max-mean'] = 2*prop - 2*prop*prop

                dataset_min_mean = dataset.dropna(subset=['ip_interval_min-mean'])
                df_down_min_mean = dataset[dataset['ip_interval_min-mean'] < line_location['min-mean'] + 1]
                df_down_count_min_mean = df_down_min_mean['ip_status'].groupby(df_down_min_mean['ip_status']).count()
                prop = df_down_count_min_mean.loc[2] / np.sum(df_down_count_min_mean.values.tolist())
                gini_dic['ip_interval']['min-mean'] = 2*prop - 2*prop*prop
                print('y = {}, gini = {}'.format(line_location, gini_dic['ip_interval']))
        if(self.type_name == 'Number'):
            if(self.frequency and self.target_name == 'ip'):
                dataset = dataset.dropna(subset=['ip_time'])
                df_down = dataset[dataset['ip_time'] < line_location + 1]
                df_down_count = df_down['ip_status'].groupby(df_down['ip_status']).count()
                prop = df_down_count.loc[2] / np.sum(df_down_count.values.tolist())
                gini_dic['ip_frequency'] = 2*prop - 2*prop*prop
                print('y = {}, gini = {}'.format(line_location, gini_dic['ip_frequency']))
            if(self.interval and self.target_name == 'ip'):
                dataset_std = dataset.dropna(subset=['ip_interval_std'])
                df_down_std = dataset[dataset['ip_interval_std'] < line_location['std'] + 1]
                df_down_count_std = df_down_std['ip_status'].groupby(df_down_std['ip_status']).count()
                prop = df_down_count_std.loc[2] / np.sum(df_down_count_std.values.tolist())
                gini_dic['ip_interval']['std'] = 2*prop - 2*prop*prop

                dataset_max_mean = dataset.dropna(subset=['ip_interval_max-mean'])
                df_down_max_mean = dataset[dataset['ip_interval_max-mean'] < line_location['max-mean'] + 1]
                df_down_count_max_mean = df_down_max_mean['ip_status'].groupby(df_down_max_mean['ip_status']).count()
                prop = df_down_count_max_mean.loc[2] / np.sum(df_down_count_max_mean.values.tolist())
                gini_dic['ip_interval']['max-mean'] = 2*prop - 2*prop*prop

                dataset_min_mean = dataset.dropna(subset=['ip_interval_min-mean'])
                df_down_min_mean = dataset[dataset['ip_interval_min-mean'] < line_location['min-mean'] + 1]
                df_down_count_min_mean = df_down_min_mean['ip_status'].groupby(df_down_min_mean['ip_status']).count()
                prop = df_down_count_min_mean.loc[2] / np.sum(df_down_count_min_mean.values.tolist())
                gini_dic['ip_interval']['min-mean'] = 2*prop - 2*prop*prop
                print('y = {}, gini = {}'.format(line_location, gini_dic['ip_interval']))
        return gini_dic