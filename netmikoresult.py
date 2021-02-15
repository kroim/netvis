from flask import Flask, render_template, redirect, url_for, request, abort, session, jsonify, send_from_directory, Response, Blueprint
from datetime import datetime
from netmiko import ConnectHandler

netmikoconfig = Blueprint('netmikoconfig', __name__)

@netmikoconfig.route('/netmikoconfig', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('netmikoconfig.html')
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
            my_device = {
            'host': "10.234.124.5",
            'username': usern,
            'password': passw,
            'device_type':'cisco_nxos',
            }
            start_time = datetime.now()
            connect = ConnectHandler(**my_device)
            out1 = connect.send_command("show ip interface brief vrf all | xml")
            out1 = out1[:-6]
            f1 = open('out1.xml','w')
            f1.write(out1)
            f1.close()
            end_time = datetime.now()            
         if case == "PDC_DCI":
            print ('It is PDC DCI')
         if case == "CDC_DCS_DCW":
            print ('It is CDC DCS DCW')
         if case == "CDC_DCI":
            print ('It is CDC DCI')
         if case == "ASH_DCS_DCW":
            print ('It is ASH DCS DCW')
         if case == "SJC_DCS_DCW":
            print ('It is SJC DCS DCW')            
         if case == "SV7_DCS_DCW":
            print ('It is SV7 DCS DCW')

    TT = "Script executed time is: {}".format(end_time - start_time)
    wrapper = """<html>
    <head>
    <title>Success!!</title>
    </head>
    <body>
    <style>
.button {
  background-color: #4CAF50;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
</style>  
<p><a href="https://192.168.1.159/netmikoconfig" class="button">Go Back</a></p><p><a href="https://192.168.1.159/" class="button">Home</a></p>
</body>
</html>"""
    return wrapper + TT