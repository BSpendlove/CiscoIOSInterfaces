from pyciscomanager import PyCiscoManager
#Import the class

# Initalize the class as a variable, this automatically sets up the SSH session and doesn't require you to keep establishing SSH sessions for a per-command function in python
mgr = PyCiscoManager('127.0.0.1', 'myUsername', 'myPassword', 22, 'mySecret')

#I can now call functions, the available functions and how to use them are on GITHUBLINKHERE
mgr.unused_interfaces(days=2)