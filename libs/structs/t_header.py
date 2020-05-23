# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

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
        self.magic = self._io.read_bytes(8)
        if not self.magic == b"\x53\x4E\x4F\x50\x53\x6F\x66\x74":
            raise kaitaistruct.ValidationNotEqualError(b"\x53\x4E\x4F\x50\x53\x6F\x66\x74", self.magic, self._io, u"/seq/0")
        self.version = self._io.read_u4le()
        self.type = self._io.read_u2le()
        self.filesize = self._io.read_u4le()
        self.filetime = self._io.read_u2le()
        self.filedate = self._io.read_u2le()
        self.foo_1 = self._io.read_u4le()
        self.foo_2 = self._io.read_u4le()
        self.crc = self._io.read_u2le()


