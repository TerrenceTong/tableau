import json
import pandas as pd

def prepare_csv(path):
    source_dic = {'time':[],'ip':[],'account':[],'status':[]}
    with open(path,'r') as f:
        list_data = json.load(f)
    for idx in range(len(list_data)):
        row = list_data[idx]['_source']
        # source_dic['idx'].append(idx)
        source_dic['time'].append(row['operationTime'].split('.')[0])
        source_dic['ip'].append(row['clientIP'])
        source_dic['account'].append('null')
        source_dic['status'].append(row['operationResult'].split(':')[1].split(',')[0][1:7])
        # print(row['operationResult'].split(':')[1].split(',')[0][1:7])
        # quit()
        # source_dic['request_type'].append(row['execution_detail']['request_type'].split(r'.')[-1])
        # source_dic['request_status'].append(row['execution_detail']['is_success'])

    # request_set = set(source_dic['request_type'])
    # print(source_dic['request_type'])
    # print(request_set)
    source_csv = pd.DataFrame(source_dic).sort_values(by=['time', 'status']).reset_index(drop=True)
    source_csv['idx'] = [i for i in range(len(list_data))]
    # print(source_csv.head())
    return source_csv

if __name__ == '__main__':
    json_dir = 'E:\\Tableau\\real_records\\LinkedIn.json'
    source_csv = prepare_csv(json_dir)
    print(source_csv.head())