# -*- coding: UTF-8 -*-
import pymysql

LOCALHOSTS = 'localhost'
USERNAME = 'root'
PASSWORD = 'root'
TABLE = 'gongli'

def insert_data_to_db(_user_id, _service_id, _role_name, _sects, _sex, _last_rename, _used_name1, _used_name2, _create_name, _gongli, _max_gongli, _gang_name, _alliance_name, _last_update):
    db = pymysql.connect(LOCALHOSTS, USERNAME, PASSWORD, TABLE, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO gongli(user_id, service_id, role_name, sects, sex, last_rename, used_name1, used_name2, create_name, gongli, max_gongli, gang_name, alliance_name, last_update) \
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s','%s')" \
    % (_user_id, _service_id, _role_name, _sects, _sex, _last_rename, _used_name1, _used_name2, _create_name, _gongli, _max_gongli, _gang_name, _alliance_name, _last_update)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # print('pass')
    except:
        db.rollback()
        # print('error')

    # 关闭数据库
    db.close()

