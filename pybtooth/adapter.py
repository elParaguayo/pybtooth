import dbus

from .constants import *

class BluetoothAdapter(object):
    def __init__(self, device):
        self.device = device
        self.props = dbus.Interface(device, PROPERTIES_IFACE)
        self.get = lambda prop: self.props.Get(ADAPTER_IFACE, prop)
        self.set = lambda prop, value: self.props.Set(ADAPTER_IFACE, prop, value)
        self.interface = dbus.Interface(device, ADAPTER_IFACE)

    def __repr__(self):
        try:
            n = self.Name
        except:
            n = "[unnamed]"

        m = self.Address

        return ("<pybtooth.device.BluetoothAdapter "
                "(name='{n}', mac='{m}')").format(n=n, m=m)

    # Methods

    def StartDiscovery(self):
        self.interface.StartDiscovery()

    def StopDiscovery(self):
        self.interface.StopDiscovery()

    def RemoveDevice(self, device):
        self.interface.RemoveDevice(device)

    def SetDiscoveryFilter(self, discovery_filter):
        self.interface.SetDiscoveryFilter(discovery_filter)

    # Properties

    @property
    def Address(self):
        return str(self.get("Address"))

    @property
    def Name(self):
        return str(self.get("Name"))

    @property
    def Alias(self):
        return str(self.get("Alias"))

    @Alias.setter
    def Alias(self, value):
        self.set("Alias", value)

    @property
    def Class(self):
        return int(self.get("Class"))

    @property
    def Powered(self):
        return bool(self.get("Powered"))

    @Powered.setter
    def Powered(self, value):
        self.set("Powered", bool(value))

    @property
    def Discoverable(self):
        return bool(self.get("Discoverable"))

    @Discoverable.setter
    def Discoverable(self, value):
        self.set("Discoverable", bool(value))

    @property
    def Pairable(self):
        return bool(self.get("Pairable"))

    @Pairable.setter
    def Pairable(self, value):
        self.set("Pairable", bool(value))

    @property
    def PairableTimeout(self):
        return int(self.get("PairableTimeout"))

    @PairableTimeout.setter
    def PairableTimeout(self, value):
        self.set("PairableTimeout", int(value))

    @property
    def DiscoverableTimeout(self):
        return int(self.get("DiscoverableTimeout"))

    @DiscoverableTimeout.setter
    def DiscoverableTimeout(self, value):
        self.set("DiscoverableTimeout", int(value))

    @property
    def Discovering(self):
        return bool(self.get("Discovering"))

    @property
    def UUIDs(self):
        return [str(x) for x in self.get("UUIDs")]

    @property
    def Modalias(self):
        try:
            return str(self.get("Modalias"))
        except:
            return None
