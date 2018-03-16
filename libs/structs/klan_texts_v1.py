# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class KlanTextsV1(KaitaiStruct):
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

    class TLinktableContentItem6(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_bytes(71)


    class TLinktableContentItem(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.mode = self._io.read_u2le()
            _on = self.mode
            if _on == 14:
                self.data = self._root.TLinktableContentItem14(self._io, self, self._root)
            elif _on == 4:
                self.data = self._root.TLinktableContentItem4(self._io, self, self._root)
            elif _on == 6:
                self.data = self._root.TLinktableContentItem6(self._io, self, self._root)
            elif _on == 13:
                self.data = self._root.TLinktableContentItem13(self._io, self, self._root)
            elif _on == 12:
                self.data = self._root.TLinktableContentItem12(self._io, self, self._root)


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

            _pos = self._io.pos()
            self._io.seek(self.param_offset)
            self._raw__m_content = self._io.read_bytes(self.param_length)
            io = KaitaiStream(BytesIO(self._raw__m_content))
            self._m_content = self._root.TLinktableContent(io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TLinktableContentItem13(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()
            self.textfile_length = self._io.read_u1()
            self.textfile = self._io.read_bytes(self.textfile_length)


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
            self._m_content = self._io.read_bytes(self.param_length)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


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


    class TLinktableContentItem12(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u4le()


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
            self.offset = self._io.read_u4le()


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
            self._m_content = self._root.TLinetableMetaContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


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
            self._m_content = self._root.TLinktableMetaContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TLinktableContentItem4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.topleft_x = self._io.read_u2le()
            self.topleft_y = self._io.read_u2le()
            self.width = self._io.read_u2le()
            self.height = self._io.read_u2le()
            self.slider_topleft_x = self._io.read_u2le()
            self.slider_topleft_y = self._io.read_u2le()
            self.slider_height = self._io.read_u2le()
            self.textfile_length = self._io.read_u1()
            self.textfile = self._io.read_bytes(self.textfile_length)


    class TLinktableContentItem14(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()
            self.value = self._io.read_u2le()


    class TLinktableContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.items = []
            i = 0
            while not self._io.is_eof():
                self.items.append(self._root.TLinktableContentItem(self._io, self, self._root))
                i += 1



    @property
    def count_linetable_meta(self):
        if hasattr(self, '_m_count_linetable_meta'):
            return self._m_count_linetable_meta if hasattr(self, '_m_count_linetable_meta') else None

        _pos = self._io.pos()
        self._io.seek((self.offset_linktable - 52))
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
                self._m_linetable_meta[i] = self._root.TLinetableMeta((self.offset_linetable_meta + (17 * i)), self._io, self, self._root)


        return self._m_linetable_meta if hasattr(self, '_m_linetable_meta') else None

    @property
    def linktable_meta(self):
        if hasattr(self, '_m_linktable_meta'):
            return self._m_linktable_meta if hasattr(self, '_m_linktable_meta') else None

        if self.count_linktable != 0:
            self._m_linktable_meta = [None] * (self.count_linktable)
            for i in range(self.count_linktable):
                self._m_linktable_meta[i] = self._root.TLinktableMeta((self.offset_linktable_meta + (20 * i)), self._io, self, self._root)


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
                self._m_palettetable[i] = self._root.TPalettetable((self.offset_palettetable + (768 * i)), self._io, self, self._root)


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

        self._m_offset_linetable_meta = (((self.offset_linktable - 52) - (self.count_linetable_meta * 17)) - 17)
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
                    self._m_linetable[i] = self._root.TLinetable(self.linetable_meta[i].content.offset, (self.offset_palettetable - self.linetable_meta[i].content.offset), self._io, self, self._root)
                else:
                    self._m_linetable[i] = self._root.TLinetable(self.linetable_meta[i].content.offset, (self.linetable_meta[(i + 1)].content.offset - self.linetable_meta[i].content.offset), self._io, self, self._root)


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
                    self._m_linktable[i] = self._root.TLinktable(self.linktable_meta[i].content.offset, (self.offset_linktable_meta - self.linktable_meta[i].content.offset), self._io, self, self._root)
                else:
                    self._m_linktable[i] = self._root.TLinktable(self.linktable_meta[i].content.offset, (self.linktable_meta[(i + 1)].content.offset - self.linktable_meta[i].content.offset), self._io, self, self._root)


        return self._m_linktable if hasattr(self, '_m_linktable') else None


