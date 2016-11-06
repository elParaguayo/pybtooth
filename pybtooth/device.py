import dbus

from .base import BluetoothBase
from .constants import *

class BluetoothDevice(BluetoothBase):
    def __init__(self, device):
        super(BluetoothDevice, self).__init__()
        self.device = device
        self.props = dbus.Interface(device, PROPERTIES_IFACE)
        self.get = lambda prop: self.props.Get(DEVICE_IFACE, prop)
        self.set = lambda prop, value: self.props.Set(DEVICE_IFACE, prop, value)
        self.interface = dbus.Interface(device, DEVICE_IFACE)

    def __repr__(self):
        try:
            n = self.Name
        except:
            n = "[unnamed]"

        m = self.Address

        return ("<pybtooth.device.BluetoothDevice "
                "(name='{n}', mac='{m}')>").format(n=n, m=m)

    # Properties
    @property
    def Address(self):
        return str(self.get("Address"))

    @property
    def Icon(self):
        try:
            return str(self.get("Icon"))
        except:
            return None

    @property
    def Class(self):
        return int(self.get("Class"))

    @property
    def Appearance(self):
        try:
            return int(self.get("Appearance"))
        except:
            return None

    @property
    def UUIDs(self):
        try:
            return [str(x) for x in self.get("UUIDs")]
        except:
            raise

    @property
    def Trusted(self):
        return bool(self.get("Trusted"))

    @Trusted.setter
    def Trusted(self, value):
        self.Trust(bool(value))

    @property
    def Connected(self):
        return bool(self.get("Connected"))

    @Connected.setter
    def Connected(self, value):
        self.Connect(bool(value))

    @property
    def Paired(self):
        return bool(self.get("Paired"))

    @property
    def Name(self):
        return str(self.get("Name"))

    @property
    def Blocked(self):
        return bool(self.get("Blocked"))

    @Blocked.setter
    def Blocked(self, value):
        self.set("Blocked", bool(value))

    @property
    def Alias(self):
        return str(self.get("Alias"))

    @Alias.setter
    def Alias(self, value):
        self.set("Alias", value)

    @property
    def Adapter(self):
        return self.get("Adapter")

    @property
    def Modalias(self):
        return str(self.get("Modalias"))

    @property
    def RSSI(self):
        try:
            return int(self.get("RSSI"))
        except:
            return None

    @property
    def LegacyPairing(self):
        return bool(self.get("LegacyPairing"))

    @property
    def TxPower(self):
        try:
            return int(self.get("TxPower"))
        except:
            return None

    @property
    def ManufacturerData(self):
        try:
            return dict(self.get("ManufacturerData"))
        except:
            return None

    @property
    def ServiceData(self):
        try:
            return dict(self.get("ServiceData"))
        except:
            return None

    @property
    def ServicesResolved(self):
        return bool(self.get("ServicesResolved"))

    # Methods

    def Connect(self, connect=True):
        if connect:
            try:
                self.interface.Connect()
                return True
            except:
                raise
                return False

        else:
            try:
                self.interface.Disconnect()
                return True
            except:
                return False

    def Disconnect(self):
        return self.Connect(False)

    def ConnectProfile(self, uuid):
        self.interface.ConnectProfile(uuid)

    def DisconnectProfile(self, uuid):
        self.interface.DisconnectProfile(uuid)

    def Trust(self, trusted=True):
        self.set("Trusted", trusted)

    def Pair(self):
        if not self.Paired:
            self.interface.Pair()
            self.Trust()

    def CancelPairing(self):
        self.interface.CancelPairing()
