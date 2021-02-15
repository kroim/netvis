from flask import Flask, render_template, redirect, url_for, request, abort, session, jsonify, send_from_directory, Response, Blueprint
import pwd_hasher
import sqlite3
from sqlite3 import Error
import json
import xmltodict
import os
import functions

import ssl
from flask import jsonify
from netmikoconfig import netmikoconfig


app = Flask(__name__)
app.secret_key = 'ffce805ea02504f5a59820c1ea8985e0432f39566059d7f8'
app.register_blueprint(netmikoconfig)
uploads_dir = os.path.join(app.static_folder, 'uploads')
vr_key = "nf:rpc-reply.nf:data.show.ip.interface.__XML__BLK_Cmd_ip_show_interface_command_brief.__XML__OPT_Cmd_ip_show_interface_command_operational.__XML__OPT_Cmd_ip_show_interface_command_vrf.__XML__OPT_Cmd_ip_show_interface_command___readonly__.__readonly__.TABLE_vrf"
int_key = "nf:rpc-reply.nf:data.show.ip.interface.__XML__BLK_Cmd_ip_show_interface_command_brief.__XML__OPT_Cmd_ip_show_interface_command_operational.__XML__OPT_Cmd_ip_show_interface_command_vrf.__XML__OPT_Cmd_ip_show_interface_command___readonly__.__readonly__.TABLE_intf"
ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'dashboard', 'submenu': ''}
        print(session)
        return render_template('dashboard.html', session=session, sidebar=sidebar)


@app.route('/pdc')
def pdc():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'pdc', 'submenu': ''}
        return render_template('pdc.html', session=session, sidebar=sidebar)

@app.route('/ash')
def ash():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'ash', 'submenu': ''}
        return render_template('ash.html', session=session, sidebar=sidebar)


@app.route('/mpls')
def mpls():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'mpls', 'submenu': ''}
        return render_template('/mpls.html', session=session, sidebar=sidebar)


@app.route('/ip_finder')
def ip_finder():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'ip_finder', 'submenu': ''}
        return render_template('ip_finder.html', session=session, sidebar=sidebar)


@app.route('/netmikoroute', methods=['POST', 'GET'])
def netmikoroute():
    if request.method == 'GET':
        return render_template('ip_finder.html')
    else:
        routing = request.form['routing']
        print(routing)
        return render_template('ip_finder.html')



@app.route('/security')
def security():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'security', 'submenu': ''}
        return render_template('security.html', session=session, sidebar=sidebar)


@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        if not session['user'][3] == 1:
            return redirect(url_for('error404'))
        table_names = functions.get_table_names()
        pci_rows = functions.get_pci()
    records = functions.get_record_time()
    sidebar = {'title': 'Netvis', 'menu': 'admin', 'submenu': ''}
    return render_template('admin.html', session=session, sidebar=sidebar, db_rows=pci_rows, table_names=table_names)


@app.route('/admin-xml', methods=['POST', 'OPTIONS'])
def admin_xml():
    if 'user' not in session:
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
                    vr_data = functions.custom_find_key(vr_key, data_dict)
                except Exception as error:
                    print("vr_data error: ", error)
                    check_vrf = 'N/A'
                    vr_data = []
                try:
                    int_data = functions.custom_find_key(int_key, data_dict)
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
                functions.db_record_time(table_name)
            return jsonify({'status': 'success', 'message': 'success added table', 'vr_data': vr_data, 'int_data': int_data}), 201
        except Exception as err:
            print("error: ", err)
            return jsonify({'status': 'error', 'message': 'Failed to upload file'})


@app.route('/admin-xml-2', methods=['POST', 'OPTIONS'])
def admin_xml_2():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'You are not logged in'})
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
        }
        return '', 200, headers
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
    table_name = request.form['table_name']
    exclude_vrf = request.form['exclude_vrf']
    exclude_ipnexthop = request.form['exclude_ipnexthop']
    map_ipnexthop = request.form['map_ipnexthop']
    table_keys = json.loads(request.form['table_keys'])
    table_fields = json.loads(request.form['table_fields'])
    filename = os.path.join(uploads_dir, file.filename)
    file.save(filename)
    table_name = table_name.replace('-', '_').strip()
    rt_res = functions.rt_to_db(xml_json_flag, filename, table_name, exclude_vrf, exclude_ipnexthop, map_ipnexthop, table_keys, table_fields)
    if rt_res['status'] == 'error':
        return jsonify(rt_res)
    return jsonify({'status': 'success', 'message': 'success added table'}), 201


@app.route('/search-ip', methods=['POST', 'OPTIONS'])
def search_ip_finder():
    if 'user' not in session:
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
        dbs = ['PDC_DCS_PRD_DSW1_CONNECTED', 'PDC_DCS_PRD_DSW2_CONNECTED', 'PDC_DCS_STG_DSW1_CONNECTED', 'PDC_DCS_STG_DSW2_CONNECTED', 'PDC_DCW_DSW1_CONNECTED', 'PDC_DCW_DSW2_CONNECTED', 'PDC_DCI_SW01_CONNECTED', 'PDC_DCI_SW02_CONNECTED', 'PDC_DCI_SW03_CONNECTED', 'PDC_DCI_SW04_CONNECTED',
               'PDC_DCS_PRD_DSW1', 'PDC_DCS_PRD_DSW2', 'PDC_DCS_STG_DSW1', 'PDC_DCS_STG_DSW2', 'PDC_DCW_DSW1', 'PDC_DCW_DSW2', 'PDC_DCI_SW01', 'PDC_DCI_SW02', 'PDC_DCI_SW03', 'PDC_DCI_SW04',
               'CDC_DCS_PRD_DSW1_CONNECTED', 'CDC_DCS_PRD_DSW2_CONNECTED', 'CDC_DCS_STG_DSW1_CONNECTED', 'CDC_DCS_STG_DSW2_CONNECTED', 'CDC_DCW_DSW1_CONNECTED', 'CDC_DCW_DSW2_CONNECTED', 'CDC_DCI_SW01_CONNECTED', 'CDC_DCI_SW02_CONNECTED', 'CDC_DCI_SW03_CONNECTED', 'CDC_DCI_SW04_CONNECTED',
			   'CDC_DCS_PRD_DSW1', 'CDC_DCS_PRD_DSW2', 'CDC_DCS_STG_DSW1', 'CDC_DCS_STG_DSW2', 'CDC_DCW_DSW1', 'CDC_DCW_DSW2', 'CDC_DCI_SW01', 'CDC_DCI_SW02', 'CDC_DCI_SW03', 'CDC_DCI_SW04',           
               'PHX_DCS_DSW1_CONNECTED', 'PHX_DCS_DSW2_CONNECTED', 'PHX_DCW_DSW1_CONNECTED', 'PHX_DCW_DSW2_CONNECTED',
               'PHX_DCS_DSW1', 'PHX_DCS_DSW2', 'PHX_DCW_DSW1', 'PHX_DCW_DSW2',
               'DFW_DCW_DSW1_CONNECTED', 'DFW_DCW_DSW2_CONNECTED', 'DFW_DCW_BSW01_CONNECTED', 'DFW_DCW_BSW02_CONNECTED', 'DFW_DCW_BSW03_CONNECTED', 'DFW_DCW_BSW04_CONNECTED', 'DFW_DCW_LSW01_CONNECTED',
               'DFW_DCW_DSW1', 'DFW_DCW_DSW2', 'DFW_DCW_BSW01', 'DFW_DCW_BSW02', 'DFW_DCW_BSW03', 'DFW_DCW_BSW04', 'DFW_DCW_LSW01',               
               'ASH_SW01_CONNECTED', 'ASH_SW02_CONNECTED', 'ASH_NX01_CONNECTED', 'ASH_NX02_CONNECTED', 'ASH_SW05_CONNECTED', 'ASH_SW06_CONNECTED',
               'ASH_SW01', 'ASH_SW02', 'ASH_NX01', 'ASH_NX02', 'ASH_SW05', 'ASH_SW06',
               'SJC_SW01_CONNECTED', 'SJC_SW02_CONNECTED', 'SJC_NX01_CONNECTED', 'SJC_NX02_CONNECTED', 'SJC_SW05_CONNECTED', 'SJC_SW06_CONNECTED',
               'SJC_SW01', 'SJC_SW02', 'SJC_NX01', 'SJC_NX02', 'SJC_SW05', 'SJC_SW06',
                #IF NOT FOUND ON ABOVE DB's SEARCH THIS DB
               'UVN'
              ]
        search_ips = functions.func_search_ip(ip_array, dbs)
        return jsonify({'status': 'success', 'message': search_ips})


@app.route('/manage-pci', methods=['POST', 'OPTIONS'])
def manage_pci():
    if 'user' not in session:
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
                    functions.db_record_time('DC_PCI')
                elif method_type == 'edit':
                    item_id = request.get_json()['id']
                    item_ip = request.get_json()['ip']
                    item_status = request.get_json()['status']
                    update_sql = "UPDATE DC_PCI SET IP = '" + item_ip + "', STATUS = '" + item_status + "' WHERE id = '" + item_id + "'"
                    cur.execute(update_sql)
                    conn.commit()
                    functions.db_record_time('DC_PCI')
                elif method_type == 'remove':
                    item_id = request.get_json()['id']
                    delete_sql = "DELETE FROM DC_PCI WHERE id = " + item_id
                    cur.execute(delete_sql)
                    conn.commit()
                    functions.db_record_time('DC_PCI')
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
    if 'user' not in session:
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
        if 'user' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    else:
        email = request.form['email']
        pwd = request.form['pwd']
        print(email, pwd)
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
                user = users[0]
                stored_pwd = user[4]
                if not pwd_hasher.verify_password(stored_pwd, pwd):
                    print('wrong password')
                    return redirect(url_for('login'))
                print("Login success")
                session['user'] = user
                print('login ok')
        except sqlite3.Error as e:
            print(e)
            conn.rollback()
        finally:
            print("finally")
            conn.close()
        return redirect(url_for('dashboard'))


@app.route('/user-manage', methods=['POST', 'GET'])
def user_management():
    if request.method == 'GET':
        if 'user' not in session:
            return redirect(url_for('login'))
        if not session['user'][3] == 1:
            return redirect(url_for('error404'))
        print(session['user'])
        if session['user'][3] != 1:
            return redirect(url_for('error404'))
        sidebar = {'title': 'User Management', 'menu': 'user-manage'}
        users = functions.db_manage_user('all', 'none', 'none')
        print("users: ", users)
        return render_template('user_management.html', session=session, sidebar=sidebar, users=users)
    else:
        if 'user' not in session:
            return jsonify({'status': 'error', 'message': 'You are not logged in'})
        if session['user'][3] != 1:
            return jsonify({'status': 'error', 'message': 'Permission is not defined'})
        method_type = request.get_json()['method_type']
        if method_type == 'edit':
            user_id = request.get_json()['user_id']
            user_role = request.get_json()['user_role']
            functions.db_manage_user('edit', user_id, user_role)
            return jsonify({'status': 'success', 'message': 'User is updated successfully'})
        elif method_type == 'remove':
            user_id = request.get_json()['user_id']
            functions.db_manage_user('remove', user_id, 'none')
            return jsonify({'status': 'success', 'message': 'User is removed successfully'})


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('dashboard'))
        return render_template('register.html')
    else:
        email = request.form['email']
        name = request.form['name']
        pwd = pwd_hasher.hash_password(request.form['pwd'])
        # user role
        role = 2
        try:
            with sqlite3.connect(database='database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO user (name, email, role, pwd) VALUES (?, ?, ?, ?)",
                            (name, email, role, pwd))
                conn.commit()
            functions.db_record_time('user')
        except:
            conn.rollback()
        finally:
            conn.close()
        return redirect(url_for('login'))


@app.route('/404', methods=['GET'])
def error404():
    return "Not found page"


if __name__ == '__main__':
    # app.secret_key = 'ffce805ea02504f5a59820c1ea8985e0432f39566059d7f8'
    # app.secret_key = "random string"
    app.run("0.0.0.0", 3000, True)
