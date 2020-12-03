import datetime
import pandas as pd

from ploter import ploter
from prepare_csv import prepare_csv


# json_dir = r'E://records_2//agents_1.json'
# csv_dir = r'E:\\Tableau\\real_records\\LinkedIn.csv'

def get_acc(data, target_ip, target_account):
    dataset = pd.DataFrame(columns=[ \
            'time', 'ip', 'account', \
                'ip_num', 'account_num', 
                    'ip_status', \
                        'account_status'], \
                                index=data['idx'])
    ip_online_time = {i:0 for i in target_ip}
    for i, item in data.iterrows():
        if(item['status'] == '900006'):
            ip_online_time[item['ip']] = 0
            dataset.loc[i]['ip_num'] = ip_online_time[item['ip']]
            dataset.loc[i]['ip_status'] = '1'
            dataset.loc[i]['time'] = item['time']
            dataset.loc[i]['ip'] = item['ip']
        if(item['status'] == '000000'):
            ip_online_time[item['ip']] += 1
            dataset.loc[i]['ip_num'] = ip_online_time[item['ip']]
            dataset.loc[i]['ip_status'] = '0'
            dataset.loc[i]['time'] = item['time']
            dataset.loc[i]['ip'] = item['ip'] 
        
    return dataset
  
if __name__ == "__main__":
    json_dir = r'E:\\Tableau\\real_records\\Twitter.json'
    csv_dir = r'E:\\Tableau\\real_records\\Twitter-acc.csv'
    source_csv = prepare_csv(json_dir)
    # print(list(set(list(source_csv['status']))))
    # quit()
    # source_csv.to_csv('E:\\Tableau\\real_records\\Twitter.csv')

    target_ip = list(set(list(source_csv['ip']))) 
    target_account = list(set(list(source_csv['account']))) 
    dataset_acc = get_acc(source_csv, target_ip, target_account)
    dataset_acc.to_csv(csv_dir, index=False)
    print('done!')
    quit()

    feature_ploter_by_time = ploter(target_ip=target_ip, target_account=target_account, t_start=0, t_stop=432000, \
        frequency = True, online_time = False, interval = False, type_name = 'Number', target_name = 'ip',\
            fre_ip_Twin = 3000, fre_ip_Nwin = 500, \
                fre_account_Twin = 3000, fre_account_Nwin = 600, \
                    online_ip_T = 86400, online_account_T = 86400,\
                        interval_ip_Twin = 3000, interval_ip_Nwin = 500, \
                            interval_account_Twin = 3000, interval_account_Nwin = 500)
    dataset_by_number = feature_ploter_by_time.get_features(source_csv)


    feature_ploter_by_time = ploter(target_ip=target_ip, target_account=target_account, t_start=0, t_stop=432000, \
        frequency = True, online_time = False, interval = False, type_name = 'Time', target_name = 'ip',\
            fre_ip_Twin = 500, fre_ip_Nwin = 600, \
                fre_account_Twin = 3000, fre_account_Nwin = 600, \
                    online_ip_T = 86400, online_account_T = 86400,\
                        interval_ip_Twin = 3000, interval_ip_Nwin = 500, \
                            interval_account_Twin = 3000, interval_account_Nwin = 500)
    dataset_by_time = feature_ploter_by_time.get_features(source_csv)

    # dataset_by_time.to_csv('./time.csv',index=False)
    # dataset_by_number.to_csv('./number.csv',index=False)