# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class TMacrosV4(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.klan2016.cz
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.type = self._io.read_u2le()
        _on = self.type
        if _on == 14:
            self.content = self._root.TMacrosV4Macro000e(self._io, self, self._root)
        elif _on == 10:
            self.content = self._root.TMacrosV4Macro000a(self._io, self, self._root)
        elif _on == 16717:
            self.content = self._root.TMacrosV4Macro414d(self._io, self, self._root)
        elif _on == 17:
            self.content = self._root.TMacrosV4Macro0011(self._io, self, self._root)
        elif _on == 4:
            self.content = self._root.TMacrosV4Macro0004(self._io, self, self._root)
        elif _on == 39:
            self.content = self._root.TMacrosV4Macro0027(self._io, self, self._root)
        elif _on == 24:
            self.content = self._root.TMacrosV4Macro0018(self._io, self, self._root)
        elif _on == 35:
            self.content = self._root.TMacrosV4Macro0023(self._io, self, self._root)
        elif _on == 6:
            self.content = self._root.TMacrosV4Macro0006(self._io, self, self._root)
        elif _on == 20:
            self.content = self._root.TMacrosV4Macro0014(self._io, self, self._root)
        elif _on == 32:
            self.content = self._root.TMacrosV4Macro0020(self._io, self, self._root)
        elif _on == 7:
            self.content = self._root.TMacrosV4Macro0007(self._io, self, self._root)
        elif _on == 1:
            self.content = self._root.TMacrosV4Macro0001(self._io, self, self._root)
        elif _on == 55:
            self.content = self._root.TMacrosV4Macro0037(self._io, self, self._root)
        elif _on == 13:
            self.content = self._root.TMacrosV4Macro000d(self._io, self, self._root)
        elif _on == 56:
            self.content = self._root.TMacrosV4Macro0038(self._io, self, self._root)
        elif _on == 45:
            self.content = self._root.TMacrosV4Macro002d(self._io, self, self._root)
        elif _on == 11:
            self.content = self._root.TMacrosV4Macro000b(self._io, self, self._root)
        elif _on == 12:
            self.content = self._root.TMacrosV4Macro000c(self._io, self, self._root)
        elif _on == 5:
            self.content = self._root.TMacrosV4Macro0005(self._io, self, self._root)
        elif _on == 33:
            self.content = self._root.TMacrosV4Macro0021(self._io, self, self._root)
        elif _on == 49407:
            self.content = self._root.TMacrosV4MacroC0ff(self._io, self, self._root)
        elif _on == 99:
            self.content = self._root.TMacrosV4Macro0063(self._io, self, self._root)
        elif _on == 19:
            self.content = self._root.TMacrosV4Macro0013(self._io, self, self._root)
        elif _on == 51:
            self.content = self._root.TMacrosV4Macro0033(self._io, self, self._root)
        elif _on == 23:
            self.content = self._root.TMacrosV4Macro0017(self._io, self, self._root)
        elif _on == 65282:
            self.content = self._root.TMacrosV4MacroFf02(self._io, self, self._root)
        elif _on == 53:
            self.content = self._root.TMacrosV4Macro0035(self._io, self, self._root)
        elif _on == 15:
            self.content = self._root.TMacrosV4Macro000f(self._io, self, self._root)
        elif _on == 38:
            self.content = self._root.TMacrosV4Macro0026(self._io, self, self._root)
        elif _on == 40:
            self.content = self._root.TMacrosV4Macro0028(self._io, self, self._root)
        elif _on == 44:
            self.content = self._root.TMacrosV4Macro002c(self._io, self, self._root)
        elif _on == 9:
            self.content = self._root.TMacrosV4Macro0009(self._io, self, self._root)
        elif _on == 240:
            self.content = self._root.TMacrosV4Macro00f0(self._io, self, self._root)
        elif _on == 21:
            self.content = self._root.TMacrosV4Macro0015(self._io, self, self._root)
        elif _on == 37:
            self.content = self._root.TMacrosV4Macro0025(self._io, self, self._root)
        elif _on == 41:
            self.content = self._root.TMacrosV4Macro0029(self._io, self, self._root)
        elif _on == 36:
            self.content = self._root.TMacrosV4Macro0024(self._io, self, self._root)
        elif _on == 18:
            self.content = self._root.TMacrosV4Macro0012(self._io, self, self._root)
        elif _on == 20302:
            self.content = self._root.TMacrosV4Macro4f4e(self._io, self, self._root)
        elif _on == 49676:
            self.content = self._root.TMacrosV4MacroC20c(self._io, self, self._root)
        elif _on == 34:
            self.content = self._root.TMacrosV4Macro0022(self._io, self, self._root)
        elif _on == 54:
            self.content = self._root.TMacrosV4Macro0036(self._io, self, self._root)
        elif _on == 43:
            self.content = self._root.TMacrosV4Macro002b(self._io, self, self._root)
        elif _on == 22:
            self.content = self._root.TMacrosV4Macro0016(self._io, self, self._root)

    class TMacrosV4Macro0015(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.topleft_x = self._io.read_u2le()
            self.topleft_y = self._io.read_u2le()
            self.bottomright_x = self._io.read_u2le()
            self.bottomright_y = self._io.read_u2le()
            self.image = self._io.read_u2le()
            self.id = self._io.read_u2le()


    class TMacrosV4Macro0004(KaitaiStruct):
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
            self.foo = self._io.read_u1()


    class TMacrosV4Macro000c(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()
            self.foo = self._io.read_u1()


    class TMacrosV4Macro0023(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.text_length = self._io.read_u1()
            self.text = self._io.read_bytes(self.text_length)
            self.foo_5 = self._io.read_u1()


    class TMacrosV4Macro0063ModeIfOnly(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_branch_if = self._io.read_bytes((self._parent.data_length_1 - 8))
            io = KaitaiStream(BytesIO(self._raw_branch_if))
            self.branch_if = self._root.TMacrosV4Macro0063BranchIf(self._parent.foo_1, io, self, self._root)


    class TMacrosV4Macro0029(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class TMacrosV4Macro0024(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TMacrosV4Macro0063BranchIf(KaitaiStruct):
        def __init__(self, param_foo_1, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.param_foo_1 = param_foo_1
            self._read()

        def _read(self):
            self.value_1 = self._io.read_u2le()
            self.condition = self._io.read_u2le()
            self.value_2 = self._io.read_u2le()
            if self.param_foo_1 == 1:
                self.foo = self._io.read_u1()

            self.macros = []
            i = 0
            while not self._io.is_eof():
                self.macros.append(TMacrosV4(self._io))
                i += 1



    class TMacrosV4MacroC20c(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class TMacrosV4Macro002c(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()
            self.textfile_length = self._io.read_u1()
            self.textfile = self._io.read_bytes(self.textfile_length)


    class TMacrosV4Macro0020(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u1()


    class TMacrosV4Macro0018(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u1()


    class TMacrosV4Macro00f0(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_bytes((self._io.size() - 2))


    class TMacrosV4Macro000f(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TMacrosV4Macro414d(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_bytes((self._io.size() - 2))


    class TMacrosV4Macro0035(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u2le()
            self.foo_6 = self._io.read_u2le()
            self.foo_7 = self._io.read_u2le()
            self.foo_8 = self._io.read_u1()


    class TMacrosV4MacroC0ff(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_bytes((self._io.size() - 2))


    class TMacrosV4Macro0014(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.textfile_length = self._io.read_u1()
            self.textfile = self._io.read_bytes(self.textfile_length)
            self.foo = self._io.read_u1()


    class TMacrosV4Macro000b(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TMacrosV4Macro0007(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u1()


    class TMacrosV4Macro0028(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TMacrosV4Macro0027(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TMacrosV4Macro002b(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u2le()
            self.foo_6 = self._io.read_u2le()
            self.foo_7 = self._io.read_u1()


    class TMacrosV4Macro0063BranchElse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.macros = []
            i = 0
            while not self._io.is_eof():
                self.macros.append(TMacrosV4(self._io))
                i += 1



    class TMacrosV4Macro0063(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_length_1 = self._io.read_u2le()
            self.data_length_2 = self._io.read_u2le()
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            _on = self.mode
            if _on == 1:
                self.branches = self._root.TMacrosV4Macro0063ModeIfElse(self._io, self, self._root)
            else:
                self.branches = self._root.TMacrosV4Macro0063ModeIfOnly(self._io, self, self._root)

        @property
        def mode(self):
            if hasattr(self, '_m_mode'):
                return self._m_mode if hasattr(self, '_m_mode') else None

            if self.data_length_2 != 0:
                self._m_mode = 1

            return self._m_mode if hasattr(self, '_m_mode') else None


    class TMacrosV4Macro0011(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.topleft_x = self._io.read_u2le()
            self.topleft_y = self._io.read_u2le()
            self.image = self._io.read_u2le()
            self.foo = self._io.read_u2le()
            self.scancode = self._io.read_u2le()


    class TMacrosV4MacroFf02(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class TMacrosV4Macro0017(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u1()


    class TMacrosV4Macro0063ModeIfElse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_branch_if = self._io.read_bytes((self._parent.data_length_2 - 8))
            io = KaitaiStream(BytesIO(self._raw_branch_if))
            self.branch_if = self._root.TMacrosV4Macro0063BranchIf(self._parent.foo_1, io, self, self._root)
            self._raw_branch_else = self._io.read_bytes((self._parent.data_length_1 - self._parent.data_length_2))
            io = KaitaiStream(BytesIO(self._raw_branch_else))
            self.branch_else = self._root.TMacrosV4Macro0063BranchElse(io, self, self._root)


    class TMacrosV4Macro0036(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TMacrosV4Macro0021(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()


    class TMacrosV4Macro002d(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u1()


    class TMacrosV4Macro0013(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TMacrosV4Macro0001(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TMacrosV4Macro0033(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.text_1_length = self._io.read_u1()
            self.text_1 = self._io.read_bytes(self.text_1_length)
            self.text_2_length = self._io.read_u1()
            self.text_2 = self._io.read_bytes(self.text_2_length)
            self.foo = self._io.read_u1()


    class TMacrosV4Macro0012(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TMacrosV4Macro0026(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TMacrosV4Macro0006(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u1()


    class TMacrosV4Macro000e(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.variable = self._io.read_u2le()
            self.value = self._io.read_u2le()


    class TMacrosV4Macro4f4e(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TMacrosV4Macro0016(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TMacrosV4Macro000d(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.variable = self._io.read_u2le()
            self.value_length = self._io.read_u1()
            self.value = self._io.read_bytes(self.value_length)


    class TMacrosV4Macro0037(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()


    class TMacrosV4Macro0005(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u2le()
            self.foo_6 = self._io.read_u1()


    class TMacrosV4Macro0009(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()
            self.image = self._io.read_u2le()
            self.foo_1 = self._io.read_u2le()
            self.topleft_x = self._io.read_u2le()
            self.topleft_y = self._io.read_u2le()
            self.scancode = self._io.read_u2le()
            self.hover_topleft_x = self._io.read_u2le()
            self.hover_topleft_y = self._io.read_u2le()
            self.hover_bottomright_x = self._io.read_u2le()
            self.hover_bottomright_y = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TMacrosV4Macro0022(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u1()


    class TMacrosV4Macro0038(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class TMacrosV4Macro000a(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u2le()
            self.foo_5 = self._io.read_u2le()
            self.foo_6 = self._io.read_u1()


    class TMacrosV4Macro0025(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()



