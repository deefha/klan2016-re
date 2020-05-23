# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import t_header
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
        self.header = t_header.THeader(self._io)
        self.fat = KlanCursors.TFat(self._io, self, self._root)
        self.data = KlanCursors.TData(self._io, self, self._root)

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
        def frames(self):
            if hasattr(self, '_m_frames'):
                return self._m_frames if hasattr(self, '_m_frames') else None

            self._m_frames = [None] * (self._parent.fat.frames_count)
            for i in range(self._parent.fat.frames_count):
                self._m_frames[i] = KlanCursors.TFrame(self._parent.fat.frames_offset, i, self._io, self, self._root)

            return self._m_frames if hasattr(self, '_m_frames') else None

        @property
        def foo_1(self):
            if hasattr(self, '_m_foo_1'):
                return self._m_foo_1 if hasattr(self, '_m_foo_1') else None

            self._m_foo_1 = KlanCursors.TFoo1(self._parent.fat.foo_1_offset, self._io, self, self._root)
            return self._m_foo_1 if hasattr(self, '_m_foo_1') else None

        @property
        def foo_2(self):
            if hasattr(self, '_m_foo_2'):
                return self._m_foo_2 if hasattr(self, '_m_foo_2') else None

            self._m_foo_2 = [None] * (self._parent.fat.foo_2_count)
            for i in range(self._parent.fat.foo_2_count):
                self._m_foo_2[i] = KlanCursors.TFoo2(self._parent.fat.foo_2[i].offset, self._io, self, self._root)

            return self._m_foo_2 if hasattr(self, '_m_foo_2') else None

        @property
        def colortables(self):
            if hasattr(self, '_m_colortables'):
                return self._m_colortables if hasattr(self, '_m_colortables') else None

            self._m_colortables = [None] * (5)
            for i in range(5):
                self._m_colortables[i] = KlanCursors.TColortable(self._parent.fat.colortables_ofset, i, self._io, self, self._root)

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
            self._m_content = KlanCursors.TFoo2Content(self._io, self, self._root)
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
            self._m_content = KlanCursors.TColortableContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None


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
            self._m_content = KlanCursors.TFoo1Content(self._io, self, self._root)
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


    class TFrameContent(KaitaiStruct):
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


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.frames_offset = self._io.read_u4le()
            self.frames_count = self._io.read_u4le()
            self.foo_1_offset = self._io.read_u4le()
            self.foo_2_count = self._io.read_u4le()
            self.colortables_ofset = self._io.read_u4le()
            self.foo = self._io.read_bytes(8)
            self.foo_2 = [None] * (99)
            for i in range(99):
                self.foo_2[i] = KlanCursors.TFatFoo2(self._io, self, self._root)



    class TFrame(KaitaiStruct):
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
            self._m_content = KlanCursors.TFrameContent(self._io, self, self._root)
            self._io.seek(_pos)
            return self._m_content if hasattr(self, '_m_content') else None



