from sqlite3 import Error
import sqlite3
import pandas as pd
import ipaddress


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
    for table_name in tables:
        table_name = table_name[0]
        # table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        # table.to_csv(table_name + '.csv', index_label='index')
        if table_name == "sqlite_sequence":
            continue
        table_names.append(table_name)
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
        return True
    elif method_type == 'remove':
        sql = "DELETE FROM user WHERE id = " + user_id
        cursor.execute(sql)
        db.commit()
        return True
    else:
        return False
