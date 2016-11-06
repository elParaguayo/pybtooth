pybtooth
========

This project is intended to provide simple, pythonic control of Bluetooth.

It is very much a work in progress so bug reporting and enhancement requests are welcome (as are pull requests...). Please use the [issues page](http://github.com/elParaguayo/pybtooth/issues).

Structure
---------
I've currently implemented the following

- BluetoothManager: This gives you control over the Bluetooth adapter and the ability to search for devices.
- BluetoothDevice: Controls for specific devices (e.g. connecting, pairing etc.)
- BluetoothMediaPlayer: Controls for media player (play, pause etc.) plus properties such as metadata

There is also an experimental signal handler for catching signals (e.g. device discovery, changing properties). The handler can be put into a thread and provide callbacks - see examples below for more.

Examples
--------

1. Show known devices and connect to one.
```
>>> from pybtooth import BluetoothManager
>>> bm = BluetoothManager()
>>> devices = bm.getDevices()
>>> print devices
[<pybtooth.device.BluetoothDevice (name='speakers', mac='AA:AA:AA:AA:AA:AA')>,
<pybtooth.device.BluetoothDevice (name='phone', mac='BB:BB:BB:BB:BB:BB')>]
>>> phone = devices[1]
>>> phone.Paired
True
>>> phone.Connected
False
>>> phone.Connect()
True
>>> print bm.getConnectedDevices()
[<pybtooth.device.BluetoothDevice (name='phone', mac='BB:BB:BB:BB:BB:BB')]
```

2. Media Player
```
>>> from pybtooth import BluetoothManager
>>> bm = BluetoothManager()
>>> mp = bm.getCurrentMediaPlayer()
>>> print mp
<pybtooth.media_player.BluetoothMediaPlayer (name='PlayerPro')>
>>> mp.Play()
>>> mp.Track
{'Album': 'Far Away Trains Passing By',
'NumberOfTracks': 0,
'Title': "Nobody's Home",
'Artist': 'Ulrich Schnauss',
'Duration': 456960,
'Genre': '',
'TrackNumber': 0}
>>> mp.Status
'playing'
```

3. Device discovery with callbacks

Code:
```
from time import sleep
from threading import Thread

from pybtooth import BluetoothSignalHandler, BluetoothManager, BT_SIGNALS
from pybtooth import constants as CONST


def device_callback(interface, path, device):
    try:
        props = man.getProperties(path)
        name = props.Get(interface, "Name")
    except:
        name = "Unknown"

    print "New device found: {} ({})".format(name, path)
    found_devices.append(device)

man = BluetoothManager()
bsh = BluetoothSignalHandler()
found_devices = []

bsh.add_callback(signal=BT_SIGNALS.SIGNAL_ADD_INTERFACE,
                 interface=CONST.DEVICE_IFACE,
                 callback=device_callback)

t = Thread(target=bsh)
t.daemon = True
t.start()

print "Starting discovery..."
man.Discover()
sleep(30)

print "Stopping..."
bsh.stop()
man.StopDiscovery()

print man.getDevices()
```

Output:
```
Starting discovery...
New device found: HTC OneX+ (/org/bluez/hci0/dev_12_34_56_78_90_AB)
Stopping...
[<pybtooth.device.BluetoothDevice (name='speakers', mac='AA:AA:AA:AA:AA:AA')>,
<pybtooth.device.BluetoothDevice (name='HTC OneX+', mac='12:34:56:78:90:AB')>,
<pybtooth.device.BluetoothDevice (name='phone', mac='BB:BB:BB:BB:BB:BB')>]
>>> dev = man.getDevices()[1]
>>> dev
<pybtooth.device.BluetoothDevice (name='HTC OneX+', mac='12:34:56:78:90:AB')>
>>> dev.Pair()
>>> dev.Paired
True
>>> dev.Trusted
True
>>> dev.Connected
False
```

To Do
-----

- Docstrings
- Probably lots of other things

elParaguayo 2016
