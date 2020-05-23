# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import t_header
class KlanDescriptions(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/popisky.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = t_header.THeader(self._io)
        self.fat = KlanDescriptions.TFat(self._io, self, self._root)
        self.data = KlanDescriptions.TData(self._io, self, self._root)

    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def descriptions(self):
            if hasattr(self, '_m_descriptions'):
                return self._m_descriptions if hasattr(self, '_m_descriptions') else None

            self._m_descriptions = [None] * (8192)
            for i in range(8192):
                self._m_descriptions[i] = KlanDescriptions.TDescription(self._parent.fat.offsets[i], self._io, self, self._root)

            return self._m_descriptions if hasattr(self, '_m_descriptions') else None


    class TDescription(KaitaiStruct):
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
                self._m_content = KlanDescriptions.TDescriptionContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TDescriptionContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = KlanDescriptions.TDescriptionData(self._io, self, self._root)


    class TDescriptionData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.title = self._io.read_bytes(128)


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u4le()
            self.foo_2 = self._io.read_u4le()
            self.foo_3 = self._io.read_u4le()
            self.foo_4 = self._io.read_u4le()
            self.offsets = [None] * (8192)
            for i in range(8192):
                self.offsets[i] = self._io.read_u4le()




