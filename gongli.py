# -*- coding:utf-8 -*-
import requests
import random
import json
import re
import pandas as pd
import math
import time
import os
from requests.adapters import HTTPAdapter
import mysql_config # 引入py文件

all_text = '' #缓存要保存字符串的容器
PAGESIZE = '100' #每页查询页数，可选参数10 25 50 100，按需修改
SAVEPAGE = 20 #获取指定页数后保存一次文件，按需修改
times_count = 0 #计次，获取指定页数后保存一次文件，无需修改
order_number = 0 #当前保存成功的文件数，默认为0，按需修改
start_page = 0 * SAVEPAGE + 1 #前面第一个数字为已保存成功的文件数，默认为0，按需修改
SAVEPATH = 'F:\\MeUser\\Desktop\\gonglibang\\' #要保存的文件夹，按需修改

# 超时重试次数
session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))

def get_data(page):
    global session

    data = {'q': 'rank', 'currentPage': page, 'pageSize': PAGESIZE, 'serviceID': '0', 'sortMethod': 'gongli', 'sortBy': 'desc', 'searchKeyword': '', 'class': '0'}
    ip = str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255))
    headers = {'Client-Ip': ip}
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S'))

        r = session.post('https://tdjingling.com/server/index.php', data=data, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        params_json = json.loads(r.text)
        params_json_data = params_json['data']
        array = re.findall(r'\\x[a-z0-9]{2}', str(params_json_data))
        json_data = str(params_json_data)

        for item in array:
            str1 = item.replace('\\', '')
            code = int("0" + str1, 16)
            character = chr(code)

            json_data = json_data.replace(item, character)

        all_json_data = json.dumps(eval(json_data))

        loads = json.loads(all_json_data, strict=False)
        c = loads['roleInfo']
        df = pd.DataFrame(c)

        global all_text

        for item in df.iloc:
            id = item[0]
            service_id = item[1]
            role_name = item[2]
            sects = item[3]
            sex = item[4]
            last_rename = item[5]
            used_name1 = item[6]
            used_name2 = item[7]
            create_name = item[8]
            gongli = item[9]
            max_gongli = item[10]
            gang_name = item[11]
            alliance_name = item[12]
            last_update = item[13]

            #① 待写入txt的字串符
            cache = str(id) + '#' + str(service_id) + '#' + str(role_name) + '#' + str(sects) + '#' + str(sex) + '#' + str(last_rename) + '#' + str(used_name1) + '#' + str(used_name2) + '#' + str(create_name) + '#' + str(gongli) + '#' + str(max_gongli) + '#' + str(gang_name) + '#' + str(alliance_name) + '#' + str(last_update) + '\n'
            all_text = all_text + cache

            #② 写入数据库
            mysql_config.insert_data_to_db(str(id), str(service_id), str(role_name), str(sects), str(sex), str(last_rename), str(used_name1), str(used_name2), str(create_name), str(gongli), str(max_gongli), str(gang_name), str(alliance_name), str(last_update))

        print(time.strftime('%Y-%m-%d %H:%M:%S'))

def task_loop():
    global all_text
    global order_number
    global start_page
    global times_count

    data = {'q': 'rank', 'currentPage': '1', 'pageSize': PAGESIZE, 'serviceID': '0', 'sortMethod': 'gongli', 'sortBy': 'desc', 'searchKeyword': '', 'class': '0'}
    ip = str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255))
    headers = {'Client-Ip': ip}
    r = requests.post('https://tdjingling.com/server/index.php', data=data, headers=headers, timeout=15)
    total = r.json()['data']['total']
    print(total)

    all_page = math.ceil(int(total) / int(PAGESIZE))
    print(all_page)

    for num in range(start_page, all_page + 1):
        print(str(num) + '/' + str(all_page))
        get_data(num)
        
        times_count = times_count + 1
        remainder = times_count % SAVEPAGE
        if num < all_page:
            if remainder == 0:
                order_number = order_number + 1
                save_to_file(all_text, order_number)
                all_text = ''
        else:
            order_number = order_number + 1
            save_to_file(all_text, order_number)
        time.sleep(0.3)

    print('数据已全部采集完毕')
    input('按回车键关闭窗口...')

# text-保存的字符串, order_number-当前保存成功的文件数
def save_to_file(text, order_number):
    is_exists = os.path.exists(SAVEPATH)
    if not is_exists:
        os.makedirs(SAVEPATH)
    file_path = SAVEPATH + 'gonglibang_' + str(order_number) + '.txt'
    fh = open(file_path, 'w', encoding='utf-8')
    fh.write(text)
    fh.close()
    print(file_path + ' save success')

task_loop()



