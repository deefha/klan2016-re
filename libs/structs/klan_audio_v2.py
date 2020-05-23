# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import t_header
class KlanAudioV2(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/zvuky.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = t_header.THeader(self._io)
        self.fat = KlanAudioV2.TFat(self._io, self, self._root)
        self.data = KlanAudioV2.TData(self._io, self, self._root)

    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def waves(self):
            if hasattr(self, '_m_waves'):
                return self._m_waves if hasattr(self, '_m_waves') else None

            self._m_waves = [None] * (8192)
            for i in range(8192):
                self._m_waves[i] = KlanAudioV2.TWave(self._parent.fat.offsets[i], self._io, self, self._root)

            return self._m_waves if hasattr(self, '_m_waves') else None


    class TWaveContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_size = self._io.read_u4le()
            self.wave_size = self._io.read_u4le()
            self.mode = self._io.read_u2le()
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u4le()
            self.data = KlanAudioV2.TWaveData(self.data_size, self._io, self, self._root)


    class TWave(KaitaiStruct):
        def __init__(self, param_offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset = param_offset
            self._read()

        def _read(self):
            pass

        @property
        def content(self):
            if hasattr(self, '_m_content'):
                return self._m_content if hasattr(self, '_m_content') else None

            if self.param_offset != 0:
                _pos = self._io.pos()
                self._io.seek(self.param_offset)
                self._m_content = KlanAudioV2.TWaveContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TWaveData(KaitaiStruct):
        def __init__(self, param_data_size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_data_size = param_data_size
            self._read()

        def _read(self):
            self.title = self._io.read_bytes(32)
            self.content = self._io.read_bytes(self.param_data_size)


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()
            self.foo_1 = self._io.read_u4le()
            self.foo_2 = self._io.read_u4le()
            self.foo_3 = self._io.read_u4le()
            self.offsets = [None] * (8192)
            for i in range(8192):
                self.offsets[i] = self._io.read_u4le()




