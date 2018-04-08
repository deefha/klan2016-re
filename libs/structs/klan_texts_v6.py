# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from t_header import THeader
class KlanTextsV6(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/texty.html
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
        def texts(self):
            if hasattr(self, '_m_texts'):
                return self._m_texts if hasattr(self, '_m_texts') else None

            self._m_texts = [None] * (500)
            for i in range(500):
                self._m_texts[i] = self._root.TText(self._parent.fat.offsets[i].offset_1, self._parent.fat.offsets[i].offset_2, self._parent.fat.offsets[i].offset_3, self._parent.fat.offsets[i].offset_4, self._io, self, self._root)

            return self._m_texts if hasattr(self, '_m_texts') else None


    class TTextContentPlain(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._io.size())


    class TText(KaitaiStruct):
        def __init__(self, param_offset_1, param_offset_2, param_offset_3, param_offset_4, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset_1 = param_offset_1
            self.param_offset_2 = param_offset_2
            self.param_offset_3 = param_offset_3
            self.param_offset_4 = param_offset_4
            self._read()

        def _read(self):
            pass

        @property
        def variants(self):
            if hasattr(self, '_m_variants'):
                return self._m_variants if hasattr(self, '_m_variants') else None

            self._m_variants = [None] * (3)
            for i in range(3):
                _on = i
                if _on == 0:
                    self._m_variants[i] = self._root.TTextVariantFull(self.param_offset_1, (self.param_offset_2 - self.param_offset_1), self._io, self, self._root)
                elif _on == 1:
                    self._m_variants[i] = self._root.TTextVariantFull(self.param_offset_2, (self.param_offset_3 - self.param_offset_2), self._io, self, self._root)
                elif _on == 2:
                    self._m_variants[i] = self._root.TTextVariantPlain(self.param_offset_3, (self.param_offset_4 - self.param_offset_3), self._io, self, self._root)

            return self._m_variants if hasattr(self, '_m_variants') else None


    class TTextVariantFull(KaitaiStruct):
        def __init__(self, param_offset, param_length, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset = param_offset
            self.param_length = param_length
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
                self._raw__m_content = self._io.read_bytes(self.param_length)
                io = KaitaiStream(BytesIO(self._raw__m_content))
                self._m_content = self._root.TTextContentFull(io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TTextVariantPlain(KaitaiStruct):
        def __init__(self, param_offset, param_length, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset = param_offset
            self.param_length = param_length
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
                self._raw__m_content = self._io.read_bytes(self.param_length)
                io = KaitaiStream(BytesIO(self._raw__m_content))
                self._m_content = self._root.TTextContentPlain(io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TTextContentFull(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._io.size())


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u2le()
            self.offsets = [None] * (500)
            for i in range(500):
                self.offsets[i] = self._root.TFatOffset(self._io, self, self._root)



    class TFatOffset(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = self._io.read_bytes(9)
            self.offset_1 = self._io.read_u4le()
            self.offset_2 = self._io.read_u4le()
            self.offset_3 = self._io.read_u4le()
            self.offset_4 = self._io.read_u4le()



