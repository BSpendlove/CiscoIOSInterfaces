import os
import textfsm
import re
from netmiko import ConnectHandler
from pprint import pprint

class PyCiscoManager(object):
    def __init__(self, ip, username, password, port=22, secret=''):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

        details = {
                'device_type' : 'cisco_ios',
                'ip' : ip,
                'username' : username,
                'password' : password,
                'port' : port
            }

        if not secret:
            print("Secret has not been configured for the specified device, function may fail...")
        else:
            details['secret'] = secret

        self.ssh_session = self.connect(details)
        self.ssh_session.enable()

    def connect(self, netmiko_dict):
        session = ConnectHandler(**netmiko_dict)
        return(session)

    def get_hostname(self):
        hostname = self.ssh_session.find_prompt()
        return(hostname.replace('>','').replace('#',''))

    def unused_interfaces(self, weeks=0, days=1):
        regex_string = "^([1-9][y])|([1-9]|[1-5][1-9])[w]([0-6])[d]|([1-9]|[1-9][0-9])[d]([1-9]|[1-2][1-9])[h]"
        if weeks is None:
            regex_string = "^([{0}-9]|[1-9][0-9])[d]([1-9]|[1-2][1-9])[h]".format(days)
        if days is None:
            regex_string = "^([1-9][y])|([{0}-9]|[1-5][1-9])[w]([0-6])[d]".format(weeks)

        all_interfaces_json = self.get_interfaces()

        for x in all_interfaces_json:
            if x['last_input'] == 'never':
                if x['last_output'] == 'never':
                    print("Interface: {0} has seen no traffic since last interface counter clear/reboot\nLast Input: {1}\nLast Output: {2}\nLast Output Hang: {3}\n".format(x['interface'], x['last_input'], x['last_output'], x['last_output_hang']))
            else:
                if re.search(regex_string, x['last_output']) is not None:
                    print("Interface: {0}\nLast Output: {1}".format(x['interface'], x['last_output']))

    #TextFSM Template functions to get data (will return JSON like formatting...)
    def get_ios_version_template(self):
        output = self.ssh_session.send_command('show version')
        return(self.textfsm_extractor('cisco_ios_show_version.template', output))

    def get_cdp_neighbors_detail_template(self):
        output = self.ssh_session.send_command('show cdp neighbors detail')
        return(self.textfsm_extractor('cisco_ios_show_cdp_neighbors_detail.template',output))

    def get_vlans_template(self):
        output = self.ssh_session.send_command('show vlan brief')
        return(self.textfsm_extractor('cisco_ios_show_vlan.template', output))

    def get_interfaces(self):
        output = self.ssh_session.send_command('show interfaces')
        return(self.textfsm_extractor('cisco_ios_show_interfaces.template', output))

    def get_hardware_model(self):
        output = self.get_ios_version_template()
        hwmodel = output[0]
        return(hwmodel['hardware'][0])

    def get_running_ios_image(self):
        output = self.get_ios_version_template()
        runningimage = output[0]
        return(runningimage['running_image'])

    def get_serial_number(self):
        output = self.get_ios_version_template()
        serialnumber = output[0]['serial'][0]
        return(serialnumber)

    def get_uptime(self):
        output = self.get_ios_version_template()
        uptime = output[0]
        return(uptime['uptime'])

    def get_version(self):
        output = self.get_ios_version_template()
        version = output[0]
        return(version['version'])

    def textfsm_extractor(self, template_name, raw_text):
        textfsm_data = list()
        fsm_handler = None

        template_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'templates'))
        template_path = '{0}/{1}'.format(template_directory, template_name)

        with open(template_path) as f:
            fsm_handler = textfsm.TextFSM(f)

            for obj in fsm_handler.ParseText(raw_text):
                entry = {}
                for index, entry_value in enumerate(obj):
                    entry[fsm_handler.header[index].lower()] = entry_value
                textfsm_data.append(entry)

            return(textfsm_data)