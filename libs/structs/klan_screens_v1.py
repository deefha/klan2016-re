# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class KlanScreensV1(KaitaiStruct):
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
        self.header = self._root.THeader(self._io, self, self._root)
        self.fat = self._root.TFat(self._io, self, self._root)
        self.data = self._root.TData(self._io, self, self._root)

    class TScreenDataCommand0007(KaitaiStruct):
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


    class TScreenDataCommand0018(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class THeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.version = self._io.read_u2le()
            self.foo = self._io.read_u2le()


    class TScreenDataBranchIf(KaitaiStruct):
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

            self.commands = []
            i = 0
            while not self._io.is_eof():
                self.commands.append(self._root.TScreenDataCommand(self._io, self, self._root))
                i += 1



    class TScreenDataCommand000b(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def screens(self):
            if hasattr(self, '_m_screens'):
                return self._m_screens if hasattr(self, '_m_screens') else None

            self._m_screens = [None] * (255)
            for i in range(255):
                self._m_screens[i] = self._root.TScreen(self._parent.fat.offsets[i], self._io, self, self._root)

            return self._m_screens if hasattr(self, '_m_screens') else None


    class TScreenDataCommand4f4e(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TScreenDataCommand000f(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TScreenDataCommand0025(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TScreenDataCommand002c(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()
            self.textfile_length = self._io.read_u1()
            self.textfile = self._io.read_bytes(self.textfile_length)


    class TScreenDataEventContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data_length = self._io.read_u2le()
            self._raw_data = self._io.read_bytes((self.data_length - 4))
            io = KaitaiStream(BytesIO(self._raw_data))
            self.data = self._root.TScreenDataEventCommands(io, self, self._root)


    class TScreenDataCommand0014(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.textfile_length = self._io.read_u1()
            self.textfile = self._io.read_bytes(self.textfile_length)
            self.foo = self._io.read_u1()


    class TScreenDataCommand0035(KaitaiStruct):
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


    class TScreenContent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type_1 = self._io.read_u1()
            self.type_2 = self._io.read_u1()
            _on = self.type_2
            if _on == 1:
                self.foo = self._io.read_u2le()
            else:
                self.foo = self._io.read_u1()
            self.data = self._root.TScreenData(self._io, self, self._root)


    class TScreenDataCommand0011(KaitaiStruct):
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


    class TScreenData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.commands = []
            i = 0
            while True:
                _ = self._root.TScreenDataCommand(self._io, self, self._root)
                self.commands.append(_)
                if _.type == 65535:
                    break
                i += 1
            self.events = []
            i = 0
            while True:
                _ = self._root.TScreenDataEvent(self._io, self, self._root)
                self.events.append(_)
                if _.binding == 65535:
                    break
                i += 1


    class TScreenDataCommand0020(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()
            self.foo_4 = self._io.read_u1()


    class TScreenDataCommand0026(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TScreenDataCommand0022(KaitaiStruct):
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


    class TScreenDataEvent(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.binding = self._io.read_u2le()
            if self.binding != 65535:
                self.content = self._root.TScreenDataEventContent(self._io, self, self._root)



    class TScreenDataCommand002b(KaitaiStruct):
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


    class TScreenDataCommand0004(KaitaiStruct):
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


    class TScreenDataCommand0015(KaitaiStruct):
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


    class TScreenDataCommand0038(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class TScreenDataCommand000c(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TScreenDataCommand0029(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u2le()


    class TScreenDataCommand0063(KaitaiStruct):
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
                self.branches = self._root.TScreenDataCommand0063ModeIfElse(self._io, self, self._root)
            else:
                self.branches = self._root.TScreenDataCommand0063ModeIfOnly(self._io, self, self._root)

        @property
        def mode(self):
            if hasattr(self, '_m_mode'):
                return self._m_mode if hasattr(self, '_m_mode') else None

            if self.data_length_2 != 0:
                self._m_mode = 1

            return self._m_mode if hasattr(self, '_m_mode') else None


    class TScreenDataCommand0027(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TScreenDataBranchElse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.commands = []
            i = 0
            while not self._io.is_eof():
                self.commands.append(self._root.TScreenDataCommand(self._io, self, self._root))
                i += 1



    class TScreenDataCommand0012(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TScreenDataCommand0023(KaitaiStruct):
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


    class TScreenDataCommand0001(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2le()


    class TScreenDataEventCommands(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.commands = []
            i = 0
            while not self._io.is_eof():
                self.commands.append(self._root.TScreenDataCommand(self._io, self, self._root))
                i += 1



    class TScreenDataCommand0033(KaitaiStruct):
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


    class TScreenDataCommand0005(KaitaiStruct):
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


    class TScreenDataCommand0037(KaitaiStruct):
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


    class TScreenDataCommand0063ModeIfOnly(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_branch_if = self._io.read_bytes((self._parent.data_length_1 - 8))
            io = KaitaiStream(BytesIO(self._raw_branch_if))
            self.branch_if = self._root.TScreenDataBranchIf(self._parent.foo_1, io, self, self._root)


    class TScreenDataCommand000d(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.variable = self._io.read_u2le()
            self.value_length = self._io.read_u1()
            self.value = self._io.read_bytes(self.value_length)


    class TScreenDataCommand0016(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TScreenDataCommand000a(KaitaiStruct):
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


    class TScreenDataCommand0024(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()


    class TScreenDataCommand0036(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TScreenDataCommand(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._io.read_u2le()
            _on = self.type
            if _on == 14:
                self.content = self._root.TScreenDataCommand000e(self._io, self, self._root)
            elif _on == 10:
                self.content = self._root.TScreenDataCommand000a(self._io, self, self._root)
            elif _on == 17:
                self.content = self._root.TScreenDataCommand0011(self._io, self, self._root)
            elif _on == 4:
                self.content = self._root.TScreenDataCommand0004(self._io, self, self._root)
            elif _on == 39:
                self.content = self._root.TScreenDataCommand0027(self._io, self, self._root)
            elif _on == 24:
                self.content = self._root.TScreenDataCommand0018(self._io, self, self._root)
            elif _on == 35:
                self.content = self._root.TScreenDataCommand0023(self._io, self, self._root)
            elif _on == 6:
                self.content = self._root.TScreenDataCommand0006(self._io, self, self._root)
            elif _on == 20:
                self.content = self._root.TScreenDataCommand0014(self._io, self, self._root)
            elif _on == 32:
                self.content = self._root.TScreenDataCommand0020(self._io, self, self._root)
            elif _on == 7:
                self.content = self._root.TScreenDataCommand0007(self._io, self, self._root)
            elif _on == 1:
                self.content = self._root.TScreenDataCommand0001(self._io, self, self._root)
            elif _on == 55:
                self.content = self._root.TScreenDataCommand0037(self._io, self, self._root)
            elif _on == 13:
                self.content = self._root.TScreenDataCommand000d(self._io, self, self._root)
            elif _on == 56:
                self.content = self._root.TScreenDataCommand0038(self._io, self, self._root)
            elif _on == 45:
                self.content = self._root.TScreenDataCommand002d(self._io, self, self._root)
            elif _on == 11:
                self.content = self._root.TScreenDataCommand000b(self._io, self, self._root)
            elif _on == 12:
                self.content = self._root.TScreenDataCommand000c(self._io, self, self._root)
            elif _on == 5:
                self.content = self._root.TScreenDataCommand0005(self._io, self, self._root)
            elif _on == 33:
                self.content = self._root.TScreenDataCommand0021(self._io, self, self._root)
            elif _on == 99:
                self.content = self._root.TScreenDataCommand0063(self._io, self, self._root)
            elif _on == 19:
                self.content = self._root.TScreenDataCommand0013(self._io, self, self._root)
            elif _on == 51:
                self.content = self._root.TScreenDataCommand0033(self._io, self, self._root)
            elif _on == 23:
                self.content = self._root.TScreenDataCommand0017(self._io, self, self._root)
            elif _on == 53:
                self.content = self._root.TScreenDataCommand0035(self._io, self, self._root)
            elif _on == 15:
                self.content = self._root.TScreenDataCommand000f(self._io, self, self._root)
            elif _on == 38:
                self.content = self._root.TScreenDataCommand0026(self._io, self, self._root)
            elif _on == 40:
                self.content = self._root.TScreenDataCommand0028(self._io, self, self._root)
            elif _on == 44:
                self.content = self._root.TScreenDataCommand002c(self._io, self, self._root)
            elif _on == 9:
                self.content = self._root.TScreenDataCommand0009(self._io, self, self._root)
            elif _on == 21:
                self.content = self._root.TScreenDataCommand0015(self._io, self, self._root)
            elif _on == 37:
                self.content = self._root.TScreenDataCommand0025(self._io, self, self._root)
            elif _on == 41:
                self.content = self._root.TScreenDataCommand0029(self._io, self, self._root)
            elif _on == 36:
                self.content = self._root.TScreenDataCommand0024(self._io, self, self._root)
            elif _on == 18:
                self.content = self._root.TScreenDataCommand0012(self._io, self, self._root)
            elif _on == 20302:
                self.content = self._root.TScreenDataCommand4f4e(self._io, self, self._root)
            elif _on == 34:
                self.content = self._root.TScreenDataCommand0022(self._io, self, self._root)
            elif _on == 54:
                self.content = self._root.TScreenDataCommand0036(self._io, self, self._root)
            elif _on == 43:
                self.content = self._root.TScreenDataCommand002b(self._io, self, self._root)
            elif _on == 22:
                self.content = self._root.TScreenDataCommand0016(self._io, self, self._root)


    class TScreenDataCommand0063ModeIfElse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_branch_if = self._io.read_bytes((self._parent.data_length_2 - 8))
            io = KaitaiStream(BytesIO(self._raw_branch_if))
            self.branch_if = self._root.TScreenDataBranchIf(self._parent.foo_1, io, self, self._root)
            self._raw_branch_else = self._io.read_bytes((self._parent.data_length_1 - self._parent.data_length_2))
            io = KaitaiStream(BytesIO(self._raw_branch_else))
            self.branch_else = self._root.TScreenDataBranchElse(io, self, self._root)


    class TScreenDataCommand0013(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()


    class TScreenDataCommand0028(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u1()


    class TScreen(KaitaiStruct):
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

            if self.param_offset != 4294967295:
                _pos = self._io.pos()
                self._io.seek(self.param_offset)
                self._m_content = self._root.TScreenContent(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_content if hasattr(self, '_m_content') else None


    class TFat(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offsets = [None] * (255)
            for i in range(255):
                self.offsets[i] = self._io.read_u4le()



    class TScreenDataCommand0017(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo = self._io.read_u1()


    class TScreenDataCommand0021(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u2le()
            self.foo_3 = self._io.read_u2le()


    class TScreenDataCommand0006(KaitaiStruct):
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


    class TScreenDataCommand002d(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.foo_1 = self._io.read_u2le()
            self.foo_2 = self._io.read_u1()


    class TScreenDataCommand000e(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.variable = self._io.read_u2le()
            self.value = self._io.read_u2le()


    class TScreenDataCommand0009(KaitaiStruct):
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
            self.foo_2 = self._io.read_u1()



