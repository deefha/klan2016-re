# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
import struct


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class THeader(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/spolecna-hlavicka.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(struct.pack('8b', 83, 78, 79, 80, 83, 111, 102, 116))
        self.version = self._io.read_u4le()
        self.type = self._io.read_u2le()
        self.filesize = self._io.read_u4le()
        self.filetime = self._io.read_u2le()
        self.filedate = self._io.read_u2le()
        self.foo_1 = self._io.read_u4le()
        self.foo_2 = self._io.read_u4le()
        self.crc = self._io.read_u2le()


