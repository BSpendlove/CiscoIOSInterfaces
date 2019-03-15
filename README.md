# CiscoIOSInterfaces
I created this script to return interfaces that are not in used for either x amount of days, or x amount of weeks but have expanded it to do a few other things. I've tried to design the script so it can be used no matter who runs it, but may need some additional tweaking for specific functions. Always feel free to give me a message if something isn't working and I'll happily have a look with you.

## How to use the script

Currently, there isn't a setup.py so if you just download all the needed files and ensure you have the following modules: textfsm and netmiko. You can import the file, here is an example:

```py
from pyciscomanager import PyCiscoManager

mgr = PyCiscoManager('192.2.0.2', 'yourUsername', 'yourPassword', 22, 'yourSecret')
mgr.unused_interfaces(weeks=8)
```

## Class Functions

### get_hostname
- Will return the hostname

```
device = mgr.get_hostname()
print(device)

Example:
SW01
```

### unused_interfaces(weeks=None,days=None)
- Will print interfaces that have not seen any output starting with x weeks or x days (weeks or days, only one works at a time)

```py
mgr.unused_interfaces(weeks=4)
```
OR
```py
mgr.unused_interfaces(days=2)
```

If interface hasn't seen traffic input or output, it will notify you.

```Example:
Device uptime: 1 week, 20 hours, 11 minutes

Interface: G1/0/10 has seen no traffic since last interface counter clear/reboot
Last Input: never
Last Output: never
Last Output Hang: never

Interface: G1/0/23 has seen no traffic since last interface counter clear/reboot
Last Input: never
Last Output: never
Last Output Hang: never
```

### get_ios_version_template
- Will return 'show version' information in JSON type format related to things like IOS Version, serial number, boot time etc..., there are additional functions that use this to get more specific information

### get_cdp_neighbors_detail_template
- Will return CDP neighbors in JSON format

### get_vlans_template
- Will return VLAN information and port members in JSON type format

### get_interfaces
- Will return interface information in JSON format

### get_hardware_model
- Will return hardware model

### get_running_ios_image
- Will return the current running IOS image

### get_serial_number
- Will return the serial number of the device

### get_uptime
- Will return the uptime of the device

### get_version
- Will return IOS version of the device