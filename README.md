# CiscoIOSInterfaces
I created this script to return interfaces that are not in used for either x amount of days, or x amount of weeks but have expanded it to do a few other things. I've tried to design the script so it can be used no matter who runs it, but may need some additional tweaking for specific functions. Always feel free to give me a message if something isn't working and I'll happily have a look with you.

## How to use the script

Currently, there isn't a setup.py so if you just download all the needed files and ensure you have the following modules: textfsm and netmiko. You can import the file, here is an example:

```py
from pyciscomanager import PyCiscoManager

mgr = PyCiscoManager('192.2.0.2', 'yourUsername', 'yourPassword', 22, 'yourSecret')
mgr.unused_interfaces(weeks=4, days=0)
```
