from sqlite3 import Error
import sqlite3
import pandas as pd
import ipaddress
import datetime


def get_current_time():
    date_string = str(datetime.datetime.now())
    return date_string.split('.')[0]


def custom_find_key(element, json_data):
    paths = element.split(".")
    for i in range(0, len(paths)):
        json_data = json_data[paths[i]]
    return json_data


def excel_database(file, table_name):
    df = pd.read_excel(file)
    df_array = df.to_numpy()
    index = 0
    with sqlite3.connect(database='database.db') as conn:
        cur = conn.cursor()
        check_table_sql = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name + "'"
        cur.execute(check_table_sql)
        if cur.fetchone()[0] == 0:
            create_table_sql = 'CREATE TABLE ' + table_name + '(id INT NOT NULL, IP CHAR(256), STATUS CHAR(256))'
            cur.execute(create_table_sql)
        for i in range(len(df_array)):
            try:
                row = df_array[i]
                ip_string = row[0]
                ips = ip_string.split('\n')
                status = row[1]
                print(index, ips, status)
                for ip in ips:
                    index = index + 1
                    insert_sql = "INSERT INTO " + table_name + "(id, IP, STATUS) VALUES ("
                    insert_sql += str(index) + ", '" + ip + "', '" + status + "')"
                    print(insert_sql)
                    cur.execute(insert_sql)
            except Exception as err:
                print(err)
    db_record_time(table_name)


def get_pci():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='DC_PCI';")
    if cursor.fetchone()[0] == 0:
        return []
    else:
        cursor.execute("SELECT * FROM DC_PCI")
        pci_rows = cursor.fetchall()
        return pci_rows


def func_search_ip(ips, dbs):
    search_res = []
    try:
        with sqlite3.connect(database='database.db') as conn:
            cur = conn.cursor()
            for ip in ips:
                pci_status = 'NO'
                pci_sql = "SELECT * FROM DC_PCI WHERE IP = '" + ip + "'"
                cur.execute(pci_sql)
                pci_res = cur.fetchall()
                if len(pci_res) > 0 and pci_status == 'NO':
                    print("len(pci_res): ", pci_res)
                    pci_status = pci_res[0][2]
                exist_flag = False
                for db in dbs:
                    cur.execute("SELECT * FROM " + db)
                    nets = cur.fetchall()
                    for net in nets:
                        if net[1] == 'N/A':
                            continue
                        if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(net[1]):
                            net = net + (pci_status,)
                            search_res.append(net)
                            exist_flag = True
                if not exist_flag:
                    search_res.append(('None', ip, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', pci_status))
            print(search_res)
    except Error as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return search_res


def get_table_names():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = []
    records = get_record_time()
    for table_name in tables:
        table_name = table_name[0]
        # table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        # table.to_csv(table_name + '.csv', index_label='index')
        if table_name == "sqlite_sequence" or table_name == "db_record_time":
            continue
        record_time = ''
        for record in records:
            if record[0] == table_name:
                record_time = record[2]
        if record_time == '':
            record_time = str(datetime.datetime.now()).split('.')[0]
        table_names.append([table_name, record_time])
    cursor.close()
    db.close()
    return table_names


def db_manage_user(method_type, user_id, role):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    if method_type == 'all':
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        users = cursor.fetchall()
        return users
    elif method_type == 'edit':
        sql = "UPDATE user SET role = '" + role + "' WHERE id = '" + user_id + "'"
        cursor.execute(sql)
        db.commit()
        db_record_time('user')
        return True
    elif method_type == 'remove':
        sql = "DELETE FROM user WHERE id = " + user_id
        cursor.execute(sql)
        db.commit()
        db_record_time('user')
        return True
    else:
        return False


def db_record_time(table_name):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    check_table_sql = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='db_record_time'"
    cursor.execute(check_table_sql)
    if cursor.fetchone()[0] == 0:
        create_table_sql = 'CREATE TABLE db_record_time (name CHAR(256) NOT NULL, created_at CHAR(256), updated_at CHAR(256))'
        cursor.execute(create_table_sql)
        db.commit()
    search_sql = "SELECT * FROM db_record_time WHERE name = '" + table_name + "'"
    cursor.execute(search_sql)
    check_table = cursor.fetchone()
    current_time = get_current_time()
    if not check_table:
        cursor.execute("INSERT INTO db_record_time (name, created_at, updated_at) VALUES (?, ?, ?)", (table_name, current_time, current_time))
        db.commit()
    else:
        update_sql = "UPDATE db_record_time SET updated_at = '" + current_time + "' WHERE name = '" + table_name + "'"
        cursor.execute(update_sql)
        db.commit()


def get_record_time():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM db_record_time")
    records = cursor.fetchall()
    return records
