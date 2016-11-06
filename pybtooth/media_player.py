import dbus

from .base import BluetoothBase
from .constants import *

class BluetoothMediaPlayer(BluetoothBase):

    TRACK_TYPES = {"Title": str,
                   "Artist": str,
                   "Album": str,
                   "Genre": str,
                   "NumberOfTracks": int,
                   "TrackNumber": int,
                   "Duration": int,}

    EQUALIZER_OFF = "off"
    EQUALIZER_ON = "on"

    REPEAT_OFF = "off"
    REPEAT_SINGLE_TRACK = "singletrack"
    REPEAT_ALL_TRACKS = "alltracks"
    REPEAT_GROUP = "group"

    SHUFFLE_OFF = "off"
    SHUFFLE_ALL_TRACKS = "alltracks"
    SHUFFLE_GROUP = "group"

    SCAN_OFF = "off"
    SCAN_ALL_TRACKS = "alltracks"
    SCAN_GROUP = "group"

    STATUS_PLAYING = "playing"
    STATUS_STOPPED = "stopped"
    STATUS_PAUSED = "paused"
    STATUS_FORWARD_SEEK = "forward-seek"
    STATUS_REVERSE_SEEK = "reverse-seek"
    STATUS_ERROR = "error"

    TYPE_AUDIO = "Audio"
    TYPE_VIDEO = "Video"
    TYPE_AUDIO_BROADCASTING = "Audio Broadcasting"
    TYPE_VIDEO_BROADCASTING = "Video Broadcasting"

    SUBTYPE_AUDIOBOOK = "Audio Book"
    SUBTYPE_PODCAST = "Podcast"

    def __init__(self, path):
        super(BluetoothMediaPlayer, self).__init__()
        self.device = dbus.SystemBus().get_object(SERVICE_NAME, path)
        self.interface = dbus.Interface(self.device, PLAYER_IFACE)
        self.props = dbus.Interface(self.device, PROPERTIES_IFACE)
        self.get = lambda prop: self.props.Get(PLAYER_IFACE, prop)
        self.set = lambda prop, value: self.props.Set(PLAYER_IFACE, prop, value)
        self.meta_template = {'Album': '',
                              'NumberOfTracks': 0,
                              'Title': '',
                              'Artist': '',
                              'Duration': 0,
                              'Genre': '',
                              'TrackNumber': 0}

    def __repr__(self):
        try:
            n = self.Name
        except:
            n = "no name"

        return ("<pybtooth.media_player.BluetoothMediaPlayer "
                "(name='{n}')>").format(n=n)

    # Methods

    def Play(self):
        self.interface.Play()

    def Stop(self):
        self.interface.Stop()

    def Pause(self):
        self.interface.Pause()

    def Next(self):
        self.interface.Next()

    def Previous(self):
        self.interface.Previous()

    def FastForward(self):
        self.interface.FastForward()

    def Rewind(self):
        self.interface.Rewind()

    # Properties

    @property
    def Equalizer(self):
        return str(self.get("Equalizer"))

    @Equalizer.setter
    def Equalizer(self, value):
        self.set("Equalizer", value)

    @property
    def Repeat(self):
        return str(self.get("Repeat"))

    @Repeat.setter
    def Repeat(self, value):
        self.set("Repeat", value)

    @property
    def Shuffle(self):
        return str(self.get("Shuffle"))

    @Shuffle.setter
    def Shuffle(self, value):
        self.set("Shuffle", value)

    @property
    def Scan(self):
        return str(self.get("Scan"))

    @Scan.setter
    def Scan(self, value):
        self.set("Scan", value)

    @property
    def Status(self):
        return str(self.get("Status"))

    @property
    def Position(self):
        return int(self.get("Position"))

    @property
    def Track(self):
        try:
            meta = self.get("Track")
            raw = {str(k): self.TRACK_TYPES[str(k)](v)
                   for k, v in meta.iteritems()}
            return raw
        except:
            return self.meta_template.copy()

    @property
    def Device(self):
        return self.get("Device")

    @property
    def Type(self):
        return str(self.get("Type"))

    @property
    def Subtype(self):
        return str(self.get("Subtype"))

    @property
    def Browsable(self):
        return bool(self.get("Browsable"))

    @property
    def Searchable(self):
        return bool(self.get("Searchable"))

    @property
    def Playlist(self):
        return self.get("Playlist")

    @property
    def Name(self):
        return str(self.get("Name"))

    @property
    def Metadata(self):
        return self.Track
