# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from t_header import THeader
class KlanMusicV2(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/hudba.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = THeader(self._io)
        self.header2 = self._root.THeader2(self._io, self, self._root)
        self.fat_mods = self._root.TFatMods(self._io, self, self._root)
        self.fat_samples = self._root.TFatSamples(self._io, self, self._root)
        self.data = self._root.TData(self._io, self, self._root)

    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.names = [None] * (128)
            for i in range(128):
                self.names[i] = self._io.read_bytes(32)


        @property
        def mods(self):
            if hasattr(self, '_m_mods'):
                return self._m_mods if hasattr(self, '_m_mods') else None

            self._m_mods = [None] * (256)
            for i in range(256):
                self._m_mods[i] = self._root.TMod(self._parent.fat_mods.offsets[i], self._io, self, self._root)

            return self._m_mods if hasattr(self, '_m_mods') else None

        @property
        def samples(self):
            if hasattr(self, '_m_samples'):
                return self._m_samples if hasattr(self, '_m_samples') else None

            self._m_samples = [None] * (1024)
            for i in range(1024):
                self._m_samples[i] = self._root.TSample(self._parent.fat_samples.offsets[i], self._io, self, self._root)

            return self._m_samples if hasattr(self, '_m_samples') else None


    class TModData(KaitaiStruct):
        def __init__(self, param_size_patterns, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_size_patterns = param_size_patterns
            self._read()

        def _read(self):
            self.samples = [None] * (256)
            for i in range(256):
                self.samples[i] = self._io.read_u2le()

            self.foo = self._io.read_bytes(80)
            self.patterns = self._io.read_bytes(self.param_size_patterns)


    class TFatSamples(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offsets = [None] * (1024)
            for i in range(1024):
                self.offsets[i] = self._io.read_u4le()



    class TSampleData(KaitaiStruct):
        def __init__(self, param_data_size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_data_size = param_data_size
            self._read()

        def _read(self):
            self.content = self._io.read_bytes(self.param_data_size)


    class TMod(KaitaiStruct):
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
                self._m_content = self._root.TModContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TFatMods(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offsets = [None] * (256)
            for i in range(256):
                self.offsets[i] = self._io.read_u4le()



    class TSample(KaitaiStruct):
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
                self._m_content = self._root.TSampleContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class THeader2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count_mods = self._io.read_u4le()
            self.count_samples = self._io.read_u4le()
            self.foo = self._io.read_bytes(24)


    class TSampleContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_size = self._io.read_u4le()
            self.foo = self._io.read_bytes(28)
            self.data = self._root.TSampleData(self.data_size, self._io, self, self._root)


    class TModContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = self._io.read_bytes(32)
            self.count_samples = self._io.read_u4le()
            self.size_patterns = self._io.read_u4le()
            self.foo_1 = self._io.read_u4le()
            self.foo_2 = self._io.read_u4le()
            self.data = self._root.TModData(self.size_patterns, self._io, self, self._root)



