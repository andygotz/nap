#
# NapDevice - PyTango device server example by Tiago to show how
#	      to implement a non-blocking command with a thread
#
from PyTango.server import Device, DeviceMeta, run
from PyTango.server import command
import time

import tangoworker


def nap(nap_time, msg="Finished sleeping"):
    time.sleep(nap_time)
    print(msg)


class NapDevice(Device):
    __metaclass__ = DeviceMeta

    @command(dtype_in=float)
    def nap(self, nap_time):
        tangoworker.execute(nap, nap_time, msg="I am finished!")


run([NapDevice])

