# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import t_macros_v3
class KlanTextV5(KaitaiStruct):
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
        pass

    class TLinetableContentPiece8(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.table = self._io.read_u1()
            self.width = self._io.read_u2le()
            self.height = self._io.read_u1()
            if self.height != 0:
                self.rows = [None] * (self.height)
                for i in range(self.height):
                    self.rows[i] = KlanTextV5.TLinetableContentPiece8Row(self._io, self, self._root)




    class TLinetableContentPiece(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.raw = self._io.read_u1()
            if  ((self.raw == 1) or (self.raw == 8) or (self.raw == 9) or (self.raw == 10) or (self.raw == 11) or (self.raw == 12) or (self.raw == 32)) :
                _on = self.raw
                if _on == 10:
                    self.data = KlanTextV5.TLinetableContentPiece8(self._io, self, self._root)
                elif _on == 32:
                    self.data = KlanTextV5.TLinetableContentPiece32(self._io, self, self._root)
                elif _on == 1:
                    self.data = KlanTextV5.TLinetableContentPiece1(self._io, self, self._root)
                elif _on == 11:
                    self.data = KlanTextV5.TLinetableContentPiece8(self._io, self, self._root)
                elif _on == 12:
                    self.data = KlanTextV5.TLinetableContentPiece8(self._io, self, self._root)
                elif _on == 8:
                    self.data = KlanTextV5.TLinetableContentPiece8(self._io, self, self._root)
                elif _on == 9:
                    self.data = KlanTextV5.TLinetableContentPiece9(self._io, self, self._root)



    class TLinktable(KaitaiStruct):
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

            if self.param_offset > 0:
                _pos = self._io.pos()
                self._io.seek(self.param_offset)
                self._m_content = KlanTextV5.TLinktableContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TLinetableContentPiece8RowData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_u1()
            if self.data > 192:
                self.addon = self._io.read_u1()



    class TLinetable(KaitaiStruct):
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

            _pos = self._io.pos()
            self._io.seek(self.param_offset)
            self._raw__m_content = self._io.read_bytes(self.param_length)
            _io__raw__m_content = KaitaiStream(BytesIO(self._raw__m_content))
            self._m_content = KlanTextV5.TLinetableContent(_io__raw__m_content, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TLinetableContentPiece1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.mode = self._io.read_u1()


    class TLinetableMetaContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.height = self._io.read_u1()
            self.top = self._io.read_u2le()
            self.foo = self._io.read_bytes(10)


    class TLinktableMetaContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.topleft_x = self._io.read_u4le()
            self.topleft_y = self._io.read_u4le()
            self.bottomright_x = self._io.read_u4le()
            self.bottomright_y = self._io.read_u4le()
            self.offset = self._io.read_s4le()


    class TLinetableContentPiece8Row(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.content = []
            i = 0
            while True:
                _ = KlanTextV5.TLinetableContentPiece8RowData(self._io, self, self._root)
                self.content.append(_)
                if _.data == 192:
                    break
                i += 1


    class TLinetableMeta(KaitaiStruct):
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

            _pos = self._io.pos()
            self._io.seek(self.param_offset)
            self._m_content = KlanTextV5.TLinetableMetaContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TLinetableContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pieces = []
            i = 0
            while not self._io.is_eof():
                self.pieces.append(KlanTextV5.TLinetableContentPiece(self._io, self, self._root))
                i += 1



    class TPalettetable(KaitaiStruct):
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

            _pos = self._io.pos()
            self._io.seek(self.param_offset)
            self._m_content = self._io.read_bytes(768)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TLinktableMeta(KaitaiStruct):
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

            _pos = self._io.pos()
            self._io.seek(self.param_offset)
            self._m_content = KlanTextV5.TLinktableMetaContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TLinetableContentPiece32(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.length = self._io.read_u1()


    class TLinktableContent(KaitaiStruct):
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
                if  ((_.type == 240) or (_.type == 16717) or (_.type == 24909) or (_.type == 49407) or (_.type == 49676) or (_.type == 65282) or (_.type == 65535)) :
                    break
                i += 1


    class TLinetableContentPiece9(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    @property
    def count_linetable_meta(self):
        if hasattr(self, '_m_count_linetable_meta'):
            return self._m_count_linetable_meta if hasattr(self, '_m_count_linetable_meta') else None

        _pos = self._io.pos()
        self._io.seek((self.offset_linktable - 212))
        self._m_count_linetable_meta = self._io.read_u4le()
        self._io.seek(_pos)
        return self._m_count_linetable_meta if hasattr(self, '_m_count_linetable_meta') else None

    @property
    def count_palettetable(self):
        if hasattr(self, '_m_count_palettetable'):
            return self._m_count_palettetable if hasattr(self, '_m_count_palettetable') else None

        _pos = self._io.pos()
        self._io.seek((self.offset_linetable_meta - 1))
        self._m_count_palettetable = self._io.read_u1()
        self._io.seek(_pos)
        return self._m_count_palettetable if hasattr(self, '_m_count_palettetable') else None

    @property
    def linetable_meta(self):
        if hasattr(self, '_m_linetable_meta'):
            return self._m_linetable_meta if hasattr(self, '_m_linetable_meta') else None

        if self.count_linetable_meta != 0:
            self._m_linetable_meta = [None] * (self.count_linetable_meta)
            for i in range(self.count_linetable_meta):
                self._m_linetable_meta[i] = KlanTextV5.TLinetableMeta((self.offset_linetable_meta + (17 * i)), self._io, self, self._root)


        return self._m_linetable_meta if hasattr(self, '_m_linetable_meta') else None

    @property
    def linktable_meta(self):
        if hasattr(self, '_m_linktable_meta'):
            return self._m_linktable_meta if hasattr(self, '_m_linktable_meta') else None

        if self.count_linktable != 0:
            self._m_linktable_meta = [None] * (self.count_linktable)
            for i in range(self.count_linktable):
                self._m_linktable_meta[i] = KlanTextV5.TLinktableMeta((self.offset_linktable_meta + (20 * i)), self._io, self, self._root)


        return self._m_linktable_meta if hasattr(self, '_m_linktable_meta') else None

    @property
    def count_linktable(self):
        if hasattr(self, '_m_count_linktable'):
            return self._m_count_linktable if hasattr(self, '_m_count_linktable') else None

        _pos = self._io.pos()
        self._io.seek((self._io.size() - 8))
        self._m_count_linktable = self._io.read_u4le()
        self._io.seek(_pos)
        return self._m_count_linktable if hasattr(self, '_m_count_linktable') else None

    @property
    def offset_linktable(self):
        if hasattr(self, '_m_offset_linktable'):
            return self._m_offset_linktable if hasattr(self, '_m_offset_linktable') else None

        _pos = self._io.pos()
        self._io.seek((self._io.size() - 4))
        self._m_offset_linktable = self._io.read_u4le()
        self._io.seek(_pos)
        return self._m_offset_linktable if hasattr(self, '_m_offset_linktable') else None

    @property
    def palettetable(self):
        if hasattr(self, '_m_palettetable'):
            return self._m_palettetable if hasattr(self, '_m_palettetable') else None

        if self.count_palettetable != 0:
            self._m_palettetable = [None] * (self.count_palettetable)
            for i in range(self.count_palettetable):
                self._m_palettetable[i] = KlanTextV5.TPalettetable((self.offset_palettetable + (768 * i)), self._io, self, self._root)


        return self._m_palettetable if hasattr(self, '_m_palettetable') else None

    @property
    def offset_linktable_meta(self):
        if hasattr(self, '_m_offset_linktable_meta'):
            return self._m_offset_linktable_meta if hasattr(self, '_m_offset_linktable_meta') else None

        self._m_offset_linktable_meta = ((self._io.size() - 8) - (20 * self.count_linktable))
        return self._m_offset_linktable_meta if hasattr(self, '_m_offset_linktable_meta') else None

    @property
    def offset_linetable_meta(self):
        if hasattr(self, '_m_offset_linetable_meta'):
            return self._m_offset_linetable_meta if hasattr(self, '_m_offset_linetable_meta') else None

        self._m_offset_linetable_meta = (((self.offset_linktable - 212) - (self.count_linetable_meta * 17)) - 17)
        return self._m_offset_linetable_meta if hasattr(self, '_m_offset_linetable_meta') else None

    @property
    def offset_palettetable(self):
        if hasattr(self, '_m_offset_palettetable'):
            return self._m_offset_palettetable if hasattr(self, '_m_offset_palettetable') else None

        self._m_offset_palettetable = ((self.offset_linetable_meta - 1) - (self.count_palettetable * 768))
        return self._m_offset_palettetable if hasattr(self, '_m_offset_palettetable') else None

    @property
    def linetable(self):
        if hasattr(self, '_m_linetable'):
            return self._m_linetable if hasattr(self, '_m_linetable') else None

        if self.count_linetable_meta != 0:
            self._m_linetable = [None] * (self.count_linetable_meta)
            for i in range(self.count_linetable_meta):
                _on = i
                if _on == (self.count_linetable_meta - 1):
                    self._m_linetable[i] = KlanTextV5.TLinetable(self.linetable_meta[i].content.offset, (self.offset_palettetable - self.linetable_meta[i].content.offset), self._io, self, self._root)
                else:
                    self._m_linetable[i] = KlanTextV5.TLinetable(self.linetable_meta[i].content.offset, (self.linetable_meta[(i + 1)].content.offset - self.linetable_meta[i].content.offset), self._io, self, self._root)


        return self._m_linetable if hasattr(self, '_m_linetable') else None

    @property
    def linktable(self):
        if hasattr(self, '_m_linktable'):
            return self._m_linktable if hasattr(self, '_m_linktable') else None

        if self.count_linktable != 0:
            self._m_linktable = [None] * (self.count_linktable)
            for i in range(self.count_linktable):
                _on = i
                if _on == (self.count_linktable - 1):
                    self._m_linktable[i] = KlanTextV5.TLinktable(self.linktable_meta[i].content.offset, (self.offset_linktable_meta - self.linktable_meta[i].content.offset), self._io, self, self._root)
                else:
                    self._m_linktable[i] = KlanTextV5.TLinktable(self.linktable_meta[i].content.offset, (self.linktable_meta[(i + 1)].content.offset - self.linktable_meta[i].content.offset), self._io, self, self._root)


        return self._m_linktable if hasattr(self, '_m_linktable') else None

    @property
    def title(self):
        if hasattr(self, '_m_title'):
            return self._m_title if hasattr(self, '_m_title') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_title = self._io.read_bytes(256)
        self._io.seek(_pos)
        return self._m_title if hasattr(self, '_m_title') else None


