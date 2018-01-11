# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from t_header import THeader
class KlanImgs(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/obrazky.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = THeader(self._io)
        self.fat = self._root.TFat(self._io, self, self._root)
        self.data = self._root.TData(self._io, self, self._root)

    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def images(self):
            if hasattr(self, '_m_images'):
                return self._m_images if hasattr(self, '_m_images') else None

            self._m_images = [None] * (8192)
            for i in range(8192):
                self._m_images[i] = self._root.TImage(self._parent.fat.offsets[i], self._io, self, self._root)

            return self._m_images if hasattr(self, '_m_images') else None


    class TImage(KaitaiStruct):
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
                self._m_content = self._root.TImageContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TImageContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_size = self._io.read_u4le()
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()
            self.mode = self._io.read_u2le()
            self.foo = self._io.read_bytes(6)
            _on = self.mode
            if _on == 257:
                self.data = self._root.TImageDataIndexed(self.data_size, self._io, self, self._root)
            elif _on == 4:
                self.data = self._root.TImageDataLossy(self.data_size, self._io, self, self._root)
            elif _on == 1:
                self.data = self._root.TImageDataIndexed(self.data_size, self._io, self, self._root)
            elif _on == 5:
                self.data = self._root.TImageDataRgb565(self.data_size, self._io, self, self._root)
            elif _on == 258:
                self.data = self._root.TImageDataCommon(self.data_size, self._io, self, self._root)
            elif _on == 256:
                self.data = self._root.TImageDataIndexed(self.data_size, self._io, self, self._root)
            elif _on == 261:
                self.data = self._root.TImageDataRgb565(self.data_size, self._io, self, self._root)


    class TImageDataIndexed(KaitaiStruct):
        def __init__(self, param_data_size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_data_size = param_data_size
            self._read()

        def _read(self):
            self.colormap = self._io.read_bytes(768)
            self.content = self._io.read_bytes((self.param_data_size - 768))


    class TImageDataRgb565(KaitaiStruct):
        def __init__(self, param_data_size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_data_size = param_data_size
            self._read()

        def _read(self):
            self.content = self._io.read_bytes(self.param_data_size)


    class TImageDataCommon(KaitaiStruct):
        def __init__(self, param_data_size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_data_size = param_data_size
            self._read()

        def _read(self):
            self.content = self._io.read_bytes(self.param_data_size)


    class TImageDataLossy(KaitaiStruct):
        def __init__(self, param_data_size, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_data_size = param_data_size
            self._read()

        def _read(self):
            self.foo = self._io.read_u4le()
            self.header_size = self._io.read_u4le()
            self.header = self._io.read_bytes(self.header_size)
            self.content = self._io.read_bytes((((self.param_data_size - 4) - 4) - self.header_size))


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




