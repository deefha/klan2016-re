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

            self._m_images = [None] * (8195)
            for i in range(8195):
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
            if _on == 1:
                self.data = self._root.TImageDataIndexed(self.data_size, self._io, self, self._root)
            elif _on == 256:
                self.data = self._root.TImageDataIndexed(self.data_size, self._io, self, self._root)
            elif _on == 257:
                self.data = self._root.TImageDataIndexed(self.data_size, self._io, self, self._root)


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


    class TMatrice(KaitaiStruct):
        def __init__(self, param_offset, param_width, param_height, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset = param_offset
            self.param_width = param_width
            self.param_height = param_height
            self._read()

        def _read(self):
            pass

        @property
        def content(self):
            if hasattr(self, '_m_content'):
                return self._m_content if hasattr(self, '_m_content') else None

            if self.param_width != 0:
                _pos = self._io.pos()
                self._io.seek(self.param_offset)
                self._m_content = self._io.read_bytes((self.param_width * self.param_height))
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()
            self.offsets = [None] * (8195)
            for i in range(8195):
                self.offsets[i] = self._io.read_u4le()



    class TCharacter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset_and_width = self._io.read_u4le()

        @property
        def computed_offset(self):
            if hasattr(self, '_m_computed_offset'):
                return self._m_computed_offset if hasattr(self, '_m_computed_offset') else None

            self._m_computed_offset = (self.offset_and_width & 16777215)
            return self._m_computed_offset if hasattr(self, '_m_computed_offset') else None

        @property
        def computed_width(self):
            if hasattr(self, '_m_computed_width'):
                return self._m_computed_width if hasattr(self, '_m_computed_width') else None

            self._m_computed_width = (self.offset_and_width >> 24)
            return self._m_computed_width if hasattr(self, '_m_computed_width') else None



