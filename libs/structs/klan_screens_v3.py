# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import t_macros_v3
class KlanScreensV3(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = KlanScreensV3.THeader(self._io, self, self._root)
        self.fat = KlanScreensV3.TFat(self._io, self, self._root)
        self.data = KlanScreensV3.TData(self._io, self, self._root)

    class THeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_u2le()
            self.foo = self._io.read_u2le()


    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def screens(self):
            if hasattr(self, '_m_screens'):
                return self._m_screens if hasattr(self, '_m_screens') else None

            self._m_screens = [None] * (1023)
            for i in range(1023):
                self._m_screens[i] = KlanScreensV3.TScreen(self._parent.fat.offsets[i], self._io, self, self._root)

            return self._m_screens if hasattr(self, '_m_screens') else None


    class TScreenDataEventContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_length = self._io.read_u2le()
            self._raw_data = self._io.read_bytes((self.data_length - 4))
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = KlanScreensV3.TScreenDataEventMacros(_io__raw_data, self, self._root)


    class TScreenContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_1 = self._io.read_u1()
            self.type_2 = self._io.read_u1()
            _on = self.type_2
            if _on == 1:
                self.foo = self._io.read_u2le()
            else:
                self.foo = self._io.read_u1()
            self.data = KlanScreensV3.TScreenData(self._io, self, self._root)


    class TScreenData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.macros = []
            i = 0
            while True:
                _ = t_macros_v3.TMacrosV3(self._io)
                self.macros.append(_)
                if _.type == 65535:
                    break
                i += 1
            self.events = []
            i = 0
            while True:
                _ = KlanScreensV3.TScreenDataEvent(self._io, self, self._root)
                self.events.append(_)
                if _.binding == 65535:
                    break
                i += 1


    class TScreenDataEvent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.binding = self._io.read_u2le()
            if self.binding != 65535:
                self.content = KlanScreensV3.TScreenDataEventContent(self._io, self, self._root)



    class TScreenDataEventMacros(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.macros = []
            i = 0
            while not self._io.is_eof():
                self.macros.append(t_macros_v3.TMacrosV3(self._io))
                i += 1



    class TScreen(KaitaiStruct):
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

            if self.param_offset != 4294967295:
                _pos = self._io.pos()
                self._io.seek(self.param_offset)
                self._m_content = KlanScreensV3.TScreenContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offsets = [None] * (1023)
            for i in range(1023):
                self.offsets[i] = self._io.read_u4le()




