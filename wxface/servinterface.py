#from dbus_next.aio import MessageBus
#import asyncio
import dbus
from dbus.exceptions import DBusException
import subprocess
import sys

#remove all async from this and use something other than dbus-next.
#try dbussy or just dbus-python

class ServInterface:

      
    def __init__(self):
        self.bus = None
        self.proxy = None
        self.interface = None
        self.active = False


    def initialize(self):
        self.bus = dbus.SessionBus()
        #print("Getting proxy object")
        try:
            self.proxy = self.bus.get_object(
                "org.memobook.memoserv1",
                "/org/memobook/memoserv1",
                introspect=True
            )
        except DBusException as d:
            print("DBusException: " + d.get_dbus_message())
        except Exception as e:
            print("Other exception: " + str(e))
        else:
            #print("Finishing with initialization")
            self.interface = dbus.Interface(self.proxy, dbus_interface="org.memobook.memoserv1")
            self.active = True


    def search(self, searchfilt):
        #response = self.proxy.Search(searchfilt)
        response = self.interface.Search(searchfilt)
        #print(response)
        return response


    def manage_wait(self, managerterm, time):
        #callstring = "busctl --user call --timeout="
        #callstring += str(time)
        #callstring += " org.memobook.memoserv1"
        #callstring += " /org/memobook/memoserv1 "
        #callstring += "Manage as "
        #callstring += str(len(managerterm))
        #callstring += " "
        #callstring += " ".join(managerterm)
        callterms = [ "busctl", "--user", "call"]
        callterms += [ "--timeout=" + str(time) ]
        callterms += [ "org.memobook.memoserv1" ]
        callterms += [ "/org/memobook/memoserv1" ]
        callterms += [ "org.memobook.memoserv1" ]
        callterms += [ "Manage" ]
        callterms += [ "as" ]
        callterms += [ str(len(managerterm)) ]
        callterms.extend(managerterm)
        try:
            complete = subprocess.run(callterms, capture_output=True, timeout=time)   
        except subprocess.CalledProcessError as cpe:
            print("Error code returned from import call")
        except subprocess.TimeoutExpired as te:
            print("Timeout value exceeded on import call")
        else:        
            if complete.returncode != 0:
                print("Return code indicates import failure")
                print("Error output: " + complete.stderr.decode(sys.stderr.encoding))
            print("Import call: " + complete.stdout.decode(sys.stdout.encoding))


# cannot, with dbus-python, get the following to work
#    def manage_wait(self, managerterm, time):
        #method = self.interface.get_dbus_method("Manage", dbus_interface="org.memobook.memoserv1")
#        print("Arg to manage is: " + str(managerterm))
        #bus_name="org.memobook.memoserv1"
        #object_path="/org/memobook/memoserv1"
        #dbus_interface="org.memobook.memoserv1"
        #method=Manage
        #signature=None ??? is in self._proxy._introspect_method_map.get(key, None)
        #args=managerterm
        #timeout=time
        #byte_arrays=False
        #**kwargs
#        from _dbus_bindings import Array, String
        #passing in func return gives 'as':<TypeError>
        #           'as' gives 'as':<TypeError>
        #           'Array' gives 'Array':<ValueError>
        #           None doesn't work either
        #           wtf is it expecting?????????
#        print("introspection: " + str(self.proxy._introspect_method_map))
#        self.bus.call_blocking("org.memobook.memoserv1",
#                                "/org/memobook/memoserv1",
#                                "org.memobook.memoserv1",
#                                "Manage",
                                #SIGNATURE
#                                self.proxy._introspect_method_map.get("org.memobook.memoserv1.Manage"),
                                #"as",
                                #dbus.Signature('as'),
                                #None,
                                #ARG
#                                Array(managerterm,"as",1),
                                #Array([String(x) for x in managerterm], dbus.Signature('as')),
                                #managerterm,
#                                time,
#                                False)
