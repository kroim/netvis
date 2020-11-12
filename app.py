from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_from_directory
import pwd_hasher
import sqlite3
from sqlite3 import Error
import json
import xmltodict
import os
import ipaddress
import functions

app = Flask(__name__)
uploads_dir = os.path.join(app.static_folder, 'uploads')
vr_key = "nf:rpc-reply.nf:data.show.ip.interface.__XML__BLK_Cmd_ip_show_interface_command_brief.__XML__OPT_Cmd_ip_show_interface_command_operational.__XML__OPT_Cmd_ip_show_interface_command_vrf.__XML__OPT_Cmd_ip_show_interface_command___readonly__.__readonly__.TABLE_vrf"
int_key = "nf:rpc-reply.nf:data.show.ip.interface.__XML__BLK_Cmd_ip_show_interface_command_brief.__XML__OPT_Cmd_ip_show_interface_command_operational.__XML__OPT_Cmd_ip_show_interface_command_vrf.__XML__OPT_Cmd_ip_show_interface_command___readonly__.__readonly__.TABLE_intf"


@app.route('/')
def dashboard():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'dashboard', 'submenu': ''}
        return render_template('dashboard.html', name=session['name'], sidebar=sidebar)


@app.route('/pdc')
def pdc():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'D 3 | PDC', 'menu': 'pdc', 'submenu': ''}
        return render_template('pdc.html', name=session['name'], sidebar=sidebar)


@app.route('/mpls')
def mpls():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'D 3 | PDC', 'menu': 'mpls', 'submenu': ''}
        return render_template('/aspath/index.html', name=session['name'], sidebar=sidebar)


@app.route('/ip_finder')
def ip_finder():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'D 3 | PDC', 'menu': 'ip_finder', 'submenu': ''}
        return render_template('ip_finder.html', name=session['name'], sidebar=sidebar)


@app.route('/admin')
def admin():
    if 'name' not in session:
        return redirect(url_for('login'))
    else:
        table_names = functions.get_table_names()
        pci_rows = []
        if 'DC_PCI' in table_names:
            with sqlite3.connect(database='database.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM DC_PCI")
                pci_rows = cur.fetchall()
        sidebar = {'title': 'Netvis', 'menu': 'admin', 'submenu': ''}
        return render_template('admin.html', name=session['name'], sidebar=sidebar, db_rows=pci_rows, table_names=table_names)


def custom_find_key(element, json_data):
    paths = element.split(".")
    for i in range(0, len(paths)):
        json_data = json_data[paths[i]]
    return json_data


@app.route('/admin-xml', methods=['POST', 'OPTIONS'])
def admin_xml():
    if 'name' not in session:
        return jsonify({'status': 'error', 'message': 'You are not logged in'})
    else:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers
        try:
            try:
                file = request.files['xml_file']
                xml_json_flag = 'xml'
            except Exception as xml_error:
                print("xml_error: ", xml_error)
                try:
                    file = request.files['json_file']
                    xml_json_flag = 'json'
                except Exception as json_error:
                    print('json_error: ', json_error)
                    return jsonify({'status': 'error', 'message': 'File is not selected'})
            if not file or not file.filename:
                return jsonify({'status': 'error', 'message': 'File is not selected'})
            print(file.filename)
            table_name = request.form['table_name']
            table_keys = json.loads(request.form['table_keys'])
            table_fields = json.loads(request.form['table_fields'])
            print("table info: ", xml_json_flag, table_name, table_keys, table_fields)
            filename = os.path.join(uploads_dir, file.filename)
            file.save(filename)
            print(filename)
            with open(filename) as file_data:
                if xml_json_flag == 'xml':
                    data_dict = xmltodict.parse(file_data.read())
                elif xml_json_flag == 'json':
                    # json_dump = json.dumps(file_data)
                    data_dict = json.load(file_data)
                else:
                    return jsonify({'status': 'error', 'message': 'Undefined file format'})
                file_data.close()
                # print(data_dict)
                check_vrf = ''
                try:
                    vr_data = custom_find_key(vr_key, data_dict)
                except Exception as error:
                    print("vr_data error: ", error)
                    check_vrf = 'N/A'
                    vr_data = []
                try:
                    int_data = custom_find_key(int_key, data_dict)
                except Exception as error:
                    print("int_data error: ", error)
                    int_data = data_dict['TABLE_intf']['ROW_intf']
                conn = sqlite3.connect('database.db')
                cur = conn.cursor()
                table_name = table_name.replace('-', '_')
                cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
                check_table = cur.fetchone()
                if check_table[0] == 1 or check_table[0] == '1':
                    print("Table already exist")
                    return jsonify({'status': 'error', 'message': 'Table already exist'})
                else:
                    create_table_sql = 'CREATE TABLE ' + table_name + '(id INT NOT NULL, IP CHAR(256), Location CHAR(256), VRF CHAR(256), '
                    for item in table_fields:
                        create_table_sql += item + " CHAR(256), "
                    create_table_sql = create_table_sql[:-2]
                    create_table_sql += ")"
                    cur.execute(create_table_sql)
                    # conn.commit()
                print("check_vrf: ", check_vrf)
                print("int_data: ", int_data)
                print("len(int_data): ", len(int_data))
                for i in range(len(int_data)):
                    if check_vrf != 'N/A':
                        vr_item = vr_data[i]['ROW_vrf']
                        item_vrf = vr_item['vrf-name-out']
                        int_item = int_data[i]['ROW_intf']
                    else:
                        int_item = int_data[i]
                        item_vrf = int_item['vrf-name-out']
                    item_id = i
                    try:
                        item_ip = int_item['subnet'] + "/" + int_item['masklen']
                    except Exception as error:
                        print("error item_ip: ", error)
                        item_ip = 'N/A'
                    item_location = table_name.replace('_', ' ')
                    insert_sql = "INSERT INTO " + table_name + " (id, IP, Location, VRF"
                    for field_item in table_fields:
                        insert_sql += ", " + field_item
                    insert_sql += ")"
                    insert_sql += " VALUES (" + str(item_id) + ", '" + item_ip + "', '" + item_location + "', '" + item_vrf
                    for field_key in table_keys:
                        try:
                            insert_sql += "', '" + int_item[field_key]
                        except Exception as error:
                            print("error tag: ", error)
                            insert_sql += "', '" + 'N/A'
                    insert_sql += "')"
                    print(insert_sql)
                    cur.execute(insert_sql)
                    conn.commit()
            return jsonify({'status': 'success', 'message': 'success added table', 'vr_data': vr_data, 'int_data': int_data}), 201
        except Exception as err:
            print("error: ", err)
            return jsonify({'status': 'error', 'message': 'Failed to upload file'})


@app.route('/search-ip', methods=['POST', 'OPTIONS'])
def search_ip_finder():
    if 'name' not in session:
        return jsonify({'status': 'error', 'message': 'You are not logged in'})
    else:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers

        ip_array = request.get_json()['ip_array']
        dbs = ['DC_CDC_DCS_PRD', 'DC_CDC_DCS_STG', 'DC_DFW_DCS', 'DC_PDC_DCS_PRD', 'DC_PDC_DCS_STG', 'DC_PHX_DCS']
        search_ips = functions.func_search_ip(ip_array, dbs)
        return jsonify({'status': 'success', 'message': search_ips})


@app.route('/manage-pci', methods=['POST', 'OPTIONS'])
def manage_pci():
    if 'name' not in session:
        return jsonify({'status': 'error', 'message': 'You are not logged in'})
    else:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers
        method_type = request.get_json()['method_type']
        try:
            with sqlite3.connect(database='database.db') as conn:
                cur = conn.cursor()
                if method_type == 'add':
                    item_ip = request.get_json()['ip']
                    item_status = request.get_json()['status']
                    insert_id = 1
                    last_sql = "SELECT * FROM DC_PCI ORDER BY id DESC LIMIT 1"
                    cur.execute(last_sql)
                    last_item = cur.fetchall()
                    if len(last_item) > 0:
                        insert_id = last_item[0][0] + 1
                    insert_sql = "INSERT INTO DC_PCI(id, IP, STATUS) VALUES (" + str(insert_id) + ", '" + item_ip + "', '" + item_status + "')"
                    cur.execute(insert_sql)
                    conn.commit()
                elif method_type == 'edit':
                    item_id = request.get_json()['id']
                    item_ip = request.get_json()['ip']
                    item_status = request.get_json()['status']
                    update_sql = "UPDATE DC_PCI SET IP = '" + item_ip + "', STATUS = '" + item_status + "' WHERE id = '" + item_id + "'"
                    cur.execute(update_sql)
                    conn.commit()
                elif method_type == 'remove':
                    item_id = request.get_json()['id']
                    delete_sql = "DELETE FROM DC_PCI WHERE id = " + item_id
                    cur.execute(delete_sql)
                    conn.commit()
                else:
                    return jsonify({'status': 'error', 'message': 'Undefined method'})
        except Exception as error:
            print(error)
            conn.rollback()
        finally:
            conn.close()

        return jsonify({'status': 'success', 'message': 'updated success'})


@app.route('/remove-table', methods=['POST', 'OPTIONS'])
def remove_table():
    if 'name' not in session:
        return jsonify({'status': 'error', 'message': 'You are not logged in'})
    else:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers
        table_name = request.get_json()['table_name']
        conn = sqlite3.connect(database='database.db')
        cursor = conn.cursor()
        drop_sql = "DROP TABLE " + table_name
        cursor.execute(drop_sql)
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': "Removed a table successfully"})


@app.route('/upload-pci', methods=['POST', 'OPTIONS'])
def upload_pci():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
        }
        return '', 200, headers
    try:
        file = request.files['pci_file']
    except Exception as pci_error:
        print("pci_error: ", pci_error)
        return jsonify({'status': 'error', 'message': 'Failed to upload file'})
    filename = os.path.join(uploads_dir, file.filename)
    file.save(filename)
    print(filename)
    functions.excel_database(filename, 'DC_PCI')
    return jsonify({'status': 'success', 'message': 'success added table'}), 201


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        # session['name'] = ''
        email = request.form['email']
        pwd = request.form['pwd']

        if email == '' or pwd == '':
            return render_template('login.html', email=email, pwd=pwd)

        try:
            with sqlite3.connect(database='database.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM user WHERE email = ?", (email,))
                users = cur.fetchall()
                if len(users) < 1:
                    print("doesn't exist")
                    return redirect(url_for('login'))

                stored_pwd = users[0][3]
                name = users[0][1]

                if not pwd_hasher.verify_password(stored_pwd, pwd):
                    print('wrong password')
                    return redirect(url_for('login'))
                session['name'] = name
                print('login ok')
        except Error as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        name = request.form['name']
        pwd = pwd_hasher.hash_password(request.form['pwd'])
        try:
            with sqlite3.connect(database='database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO user (name, email, pwd) VALUES (?, ?, ?)",
                            (name, email, pwd))
                conn.commit()
        except:
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('login'))


if __name__ == '__main__':
    # app.secret_key = 'ffce805ea02504f5a59820c1ea8985e0432f39566059d7f8'
    app.secret_key = "random string"
    app.run("127.0.0.1", 3000, True)
