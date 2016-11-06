from .base import BluetoothBase
from .constants import *
from .device import BluetoothDevice
from .media_player import BluetoothMediaPlayer

class BluetoothManager(BluetoothBase):

    def __init__(self):
        super(BluetoothManager, self).__init__()
        self.devices = self.getDevices()

    def getDevices(self):
        devices = self._findInterface(DEVICE_IFACE)
        return [BluetoothDevice(self._getDevice(x)) for x in devices]

    def getConnectedDevices(self):
        devices = self.getNamedDevices()
        bd = [BluetoothDevice(self._getDevice(x)) for x in devices]
        return [x for x in bd if x.connected]

    def getNamedDevices(self):
        devices = self.getDevices()
        nd = []
        for device in devices:
            try:
                name = device.name
                nd.append(device)
            except:
                pass

        return nd

    def getCurrentMediaPlayer(self):
        mp = self._findInterface(PLAYER_IFACE)
        if mp:
            return BluetoothMediaPlayer(str(mp[0]))
        else:
            return None

    def Discover(self, timeout=None):
        if timeout:
            self.adapter.DiscoverableTimeout = timeout

        if self.adapter:
            self.adapter.StartDiscovery()

    def StopDiscovery(self):
        self.adapter.StopDiscovery()

    def Forget(self, device):
        try:
            self.adapter.RemoveDevice(device.interface)
            return True
        except:
            return False

    def SetDiscoveryFilter(self, discovery_filter):
        self.adapter.SetDiscoveryFilter(discovery_filter)

    @property
    def Address(self):
        pass
