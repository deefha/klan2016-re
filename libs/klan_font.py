# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from t_header import THeader
class KlanFont(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/fonty.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = THeader(self._io)
        self.fat = self._root.TFat(self._io, self, self._root)

    class TMatrix(KaitaiStruct):
        def __init__(self, width, height, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.width = width
            self.height = height
            self._read()

        def _read(self):
            self.rows = [None] * (self.height)
            for i in range(self.height):
                self.rows[i] = self._root.TRow(self.width, self._io, self, self._root)



    class TColor(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_u1()
            self.g = self._io.read_u1()
            self.b = self._io.read_u1()


    class TRow(KaitaiStruct):
        def __init__(self, width, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.width = width
            self._read()

        def _read(self):
            self.columns = [None] * (self.width)
            for i in range(self.width):
                self.columns[i] = self._io.read_u1()



    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()
            self.foo_1 = self._io.read_bytes(16)
            self.offsets = [None] * (59)
            for i in range(59):
                self.offsets[i] = self._io.read_u4le()



    class TFont(KaitaiStruct):
        def __init__(self, offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.offset = offset
            self._read()

        def _read(self):
            self.datalength = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.colors = [None] * (256)
            for i in range(256):
                self.colors[i] = self._root.TColor(self._io, self, self._root)

            self.characters = [None] * (256)
            for i in range(256):
                self.characters[i] = self._root.TCharacter(self._io, self, self._root)


        @property
        def matrices(self):
            if hasattr(self, '_m_matrices'):
                return self._m_matrices if hasattr(self, '_m_matrices') else None

            _pos = self._io.pos()
            self._m_matrices = [None] * (256)
            for i in range(256):
                if self.characters[i].width != 0:
                    self._io.seek(((((self.offset + 8) + 768) + 1024) + self.characters[i].offset))
                    self._m_matrices[i] = self._root.TMatrix(self.characters[i].width, self.height, self._io, self, self._root)

            self._io.seek(_pos)

            return self._m_matrices if hasattr(self, '_m_matrices') else None


    class TCharacter(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset_and_width = self._io.read_u4le()

        @property
        def offset(self):
            if hasattr(self, '_m_offset'):
                return self._m_offset if hasattr(self, '_m_offset') else None

            self._m_offset = (self.offset_and_width & 16777215)
            return self._m_offset if hasattr(self, '_m_offset') else None

        @property
        def width(self):
            if hasattr(self, '_m_width'):
                return self._m_width if hasattr(self, '_m_width') else None

            self._m_width = (self.offset_and_width >> 24)
            return self._m_width if hasattr(self, '_m_width') else None


    @property
    def fonts(self):
        if hasattr(self, '_m_fonts'):
            return self._m_fonts if hasattr(self, '_m_fonts') else None

        _pos = self._io.pos()
        self._m_fonts = [None] * (59)
        for i in range(59):
            if self.fat.offsets[i] != 0:
                self._io.seek(self.fat.offsets[i])
                self._m_fonts[i] = self._root.TFont(self.fat.offsets[i], self._io, self, self._root)

        self._io.seek(_pos)

        return self._m_fonts if hasattr(self, '_m_fonts') else None


