from flask import Flask, render_template, redirect, url_for, request, abort, session, jsonify, send_from_directory, Response, Blueprint
from datetime import datetime
from netmiko import ConnectHandler

netmikoconfig = Blueprint('netmikoconfig', __name__)

@netmikoconfig.route('/netmikoconfig', methods=['POST', 'GET'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        sidebar = {'title': 'Netvis', 'menu': 'settings', 'submenu': 'configuration'}
        if request.method == 'GET':
            return render_template('netmikoconfig.html', session=session, sidebar=sidebar)
        else:
            usern = request.form['usern']
            passw = request.form['passw']
            PDC_NETMIKO = request.form.get('PDC_NETMIKO')
            CDC_NETMIKO = request.form.get('CDC_NETMIKO')
            ASH_NETMIKO = request.form.get('ASH_NETMIKO')
            SJC_NETMIKO = request.form.get('SJC_NETMIKO')
            SV7_NETMIKO = request.form.get('SV7_NETMIKO')
            LOGIN_DB = [PDC_NETMIKO, CDC_NETMIKO, ASH_NETMIKO, SJC_NETMIKO, SV7_NETMIKO]
            start_time = (0)
            end_time = (0)
            print(LOGIN_DB)
            for case in LOGIN_DB:
                if case == "PDC_DCS_DCW":
                    # IP-FINDER SECTION
                    start_time = datetime.now()
                    # DCS
                    config = {
                        'host': "10.234.124.11",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/prd/DSW1-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/prd/DSW1.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.12",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/prd/DSW2-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/prd/DSW2.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.13",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/stg/DSW1-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/stg/DSW1.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.14",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/stg/DSW2-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcs/stg/DSW2.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    # DCW
                    config = {
                        'host': "10.234.127.5",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                        # 'session_log': 'my_file.out',
                        "fast_cli": False,
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcw/DCW1-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcw/DCW1.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.127.6",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                        "fast_cli": False,
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcw/DCW2-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dcw/DCW2.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    end_time = datetime.now()
                if case == "PDC_DCI":
                    # IP-FINDER SECTION
                    start_time = datetime.now()

                    config = {
                        'host': "10.234.124.51",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW01-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW01.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.52",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW02-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW02.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.53",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW03-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW03.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.54",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW04-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW04.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.55",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW05-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW05.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.234.124.56",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW06-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/pdc/dci/SW06.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    end_time = datetime.now()

                if case == "CDC_DCS_DCW":
                    # IP-FINDER SECTION
                    start_time = datetime.now()
                    # DCS
                    config = {
                        'host': "10.232.124.11",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/prd/DSW1-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/prd/DSW1.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.232.124.12",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/prd/DSW2-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/prd/DSW2.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.232.124.13",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/stg/DSW1-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/stg/DSW1.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.232.124.14",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/stg/DSW2-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcs/stg/DSW2.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    # DCW
                    config = {
                        'host': "10.232.124.5",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                        # 'session_log': 'my_file.out',
                        "fast_cli": False,
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcw/DCW1-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcw/DCW1.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    config = {
                        'host': "10.232.124.6",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                        "fast_cli": False,
                    }
                    connect = ConnectHandler(**config)
                    config = connect.send_command("show ip interface vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcw/DCW2-CONNECTED.xml', 'w')
                    config_file.write(config)
                    config_file.close()
                    config = connect.send_command("show ip route vrf all | xml")
                    config = config[:-6]
                    config_file = open('static/dc/ipfinder/cdc/dcw/DCW2.xml', 'w')
                    config_file.write(config)
                    config_file.close()

                    end_time = datetime.now()

                if case == "CDC_DCI":
                    print('It is CDC DCI')
                if case == "ASH_DCS_DCW":
                    # IP-FINDER SECTION
                    # <Code here>
                    # VISIO SECTION
                    start_time = datetime.now()
                    R01 = {
                        'host': "10.111.249.195",
                        'username': usern,
                        'password': passw,
                        'device_type': 'cisco_nxos',
                    }
                    connect = ConnectHandler(**R01)
                    R01 = connect.send_command("show ip interface brief")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-C.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 10.111.40.121 received-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-ATTN-B-R.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 10.111.40.121 advertised-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-ATTN-B-A.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 172.31.253.245 received-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-ATTT-B-R.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 172.31.253.245 advertised-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-ATTT-B-A.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 10.82.28.1 received-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-SW01-B-R.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 10.82.28.1 advertised-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-SW01-B-A.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 10.82.28.3 received-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-SW02-B-R.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    R01 = connect.send_command("show ip bgp neighbors 10.82.28.3 advertised-routes")
                    f1 = open('static/dc/visio/ash/R01-R02/R01-SW02-B-A.txt', 'w')
                    f1.write(R01)
                    f1.close()
                    end_time = datetime.now()
                if case == "SJC_DCS_DCW":
                    print('It is SJC DCS DCW')
                if case == "SV7_DCS_DCW":
                    print('It is SV7 DCS DCW')

        TT = "Script executed time is: {}".format(end_time - start_time)
        return render_template('netmikoresult.html', TT=TT, session=session, sidebar=sidebar)
        # return wrapper + TT
