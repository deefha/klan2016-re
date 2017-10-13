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
        def fonts(self):
            if hasattr(self, '_m_fonts'):
                return self._m_fonts if hasattr(self, '_m_fonts') else None

            self._m_fonts = [None] * (63)
            for i in range(63):
                self._m_fonts[i] = self._root.TFont(self._parent.fat.offsets[i], self._io, self, self._root)

            return self._m_fonts if hasattr(self, '_m_fonts') else None


    class TMatrices(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.matrices = [None] * (256)
            for i in range(256):
                self.matrices[i] = self._root.TMatrice(self._parent.characters[i].offset, self._parent.characters[i].width, self._parent.height, self._io, self, self._root)



    class TFontBody(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.matrices_size = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.colormap = self._io.read_bytes(768)
            self.characters = [None] * (256)
            for i in range(256):
                self.characters[i] = self._root.TCharacter(self._io, self, self._root)

            self._raw_matrices = self._io.read_bytes(self.matrices_size)
            io = KaitaiStream(BytesIO(self._raw_matrices))
            self.matrices = self._root.TMatrices(io, self, self._root)


    class TMatrice(KaitaiStruct):
        def __init__(self, matrice_offset, matrice_width, matrice_height, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.matrice_offset = matrice_offset
            self.matrice_width = matrice_width
            self.matrice_height = matrice_height
            self._read()

        def _read(self):
            pass

        @property
        def body(self):
            if hasattr(self, '_m_body'):
                return self._m_body if hasattr(self, '_m_body') else None

            if self.matrice_width != 0:
                _pos = self._io.pos()
                self._io.seek(self.matrice_offset)
                self._m_body = self._io.read_bytes((self.matrice_width * self.matrice_height))
                self._io.seek(_pos)

            return self._m_body if hasattr(self, '_m_body') else None


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4le()
            self.offsets = [None] * (63)
            for i in range(63):
                self.offsets[i] = self._io.read_u4le()



    class TFont(KaitaiStruct):
        def __init__(self, font_offset, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.font_offset = font_offset
            self._read()

        def _read(self):
            pass

        @property
        def body(self):
            if hasattr(self, '_m_body'):
                return self._m_body if hasattr(self, '_m_body') else None

            if self.font_offset != 0:
                _pos = self._io.pos()
                self._io.seek(self.font_offset)
                self._m_body = self._root.TFontBody(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_body if hasattr(self, '_m_body') else None


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



