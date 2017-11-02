# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from t_header import THeader
class KlanCursors(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz/knihovny/kurzory.html
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

    class TColortableContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(768)


    class TFoo1Content(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(512)


    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def cursors(self):
            if hasattr(self, '_m_cursors'):
                return self._m_cursors if hasattr(self, '_m_cursors') else None

            self._m_cursors = [None] * (self._parent.fat.cursors_count)
            for i in range(self._parent.fat.cursors_count):
                self._m_cursors[i] = self._root.TCursor(self._parent.fat.cursors_offset, i, self._io, self, self._root)

            return self._m_cursors if hasattr(self, '_m_cursors') else None

        @property
        def foo_1(self):
            if hasattr(self, '_m_foo_1'):
                return self._m_foo_1 if hasattr(self, '_m_foo_1') else None

            self._m_foo_1 = self._root.TFoo1(self._parent.fat.foo_1_offset, self._io, self, self._root)
            return self._m_foo_1 if hasattr(self, '_m_foo_1') else None

        @property
        def foo_2(self):
            if hasattr(self, '_m_foo_2'):
                return self._m_foo_2 if hasattr(self, '_m_foo_2') else None

            self._m_foo_2 = [None] * (self._parent.fat.foo_2_count)
            for i in range(self._parent.fat.foo_2_count):
                self._m_foo_2[i] = self._root.TFoo2(self._parent.fat.foo_2[i].offset, self._io, self, self._root)

            return self._m_foo_2 if hasattr(self, '_m_foo_2') else None

        @property
        def colortables(self):
            if hasattr(self, '_m_colortables'):
                return self._m_colortables if hasattr(self, '_m_colortables') else None

            self._m_colortables = [None] * (5)
            for i in range(5):
                self._m_colortables[i] = self._root.TColortable(self._parent.fat.colortables_ofset, i, self._io, self, self._root)

            return self._m_colortables if hasattr(self, '_m_colortables') else None


    class TFoo2Content(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(31)


    class TFoo2(KaitaiStruct):
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
            self._m_content = self._root.TFoo2Content(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TColortable(KaitaiStruct):
        def __init__(self, param_offset, param_index, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset = param_offset
            self.param_index = param_index
            self._read()

        def _read(self):
            pass

        @property
        def content(self):
            if hasattr(self, '_m_content'):
                return self._m_content if hasattr(self, '_m_content') else None

            _pos = self._io.pos()
            self._io.seek((self.param_offset + (self.param_index * 768)))
            self._m_content = self._root.TColortableContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TCursorContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_u1()
            self.y = self._io.read_u1()
            self.id = self._io.read_u2le()
            self.data = self._io.read_bytes(1024)


    class TFoo1(KaitaiStruct):
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
            self._m_content = self._root.TFoo1Content(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TCursor(KaitaiStruct):
        def __init__(self, param_offset, param_index, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_offset = param_offset
            self.param_index = param_index
            self._read()

        def _read(self):
            pass

        @property
        def content(self):
            if hasattr(self, '_m_content'):
                return self._m_content if hasattr(self, '_m_content') else None

            _pos = self._io.pos()
            self._io.seek((self.param_offset + (self.param_index * (((1 + 1) + 2) + 1024))))
            self._m_content = self._root.TCursorContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


    class TFatFoo2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u4le()
            self.foo = self._io.read_u4le()


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cursors_offset = self._io.read_u4le()
            self.cursors_count = self._io.read_u4le()
            self.foo_1_offset = self._io.read_u4le()
            self.foo_2_count = self._io.read_u4le()
            self.colortables_ofset = self._io.read_u4le()
            self.foo = self._io.read_bytes(8)
            self.foo_2 = [None] * (99)
            for i in range(99):
                self.foo_2[i] = self._root.TFatFoo2(self._io, self, self._root)




