from ctypes import *

import six

from .map import maps


class GW2Context(Structure):
    _fields_ = [
        ("serverAddress", c_char * 28),
        ("mapId", c_uint32),
        ("mapType", c_uint32),
        ("shardId", c_uint32),
        ("instance", c_uint32),
        ("buildId", c_uint32),
    ]


class LinkedMem(Structure):
    _fields_ = [
        ("uiVersion", c_uint32),
        ("uiTick", c_uint32),
        ("fAvatarPosition", c_float * 3),
        ("fAvatarFront", c_float * 3),
        ("fAvatarTop", c_float * 3),
        ("name", c_wchar * 256),
        ("fCameraPosition", c_float * 3),
        ("fCameraFront", c_float * 3),
        ("fCameraTop", c_float * 3),
        ("identity", c_wchar * 256),
        ("context_len", c_uint32),
        # ("context", c_char * 256),
        ("context", GW2Context),
        ("context_padding", c_char * (256 - sizeof(GW2Context))),
        ("description", c_wchar * 2048),
    ]


FILE_MAP_ALL_ACCESS = 0x1F
PAGE_READ_WRITE = 0x04
INVALID_HANDLE_VALUE = -1


class FileMapping(object):
    def __init__(self, name, value_struct, create=True):
        super(FileMapping, self).__init__()

        if not isinstance(name, six.text_type):
            name = six.text_type(name)

        size = sizeof(value_struct)
        pointer_type = POINTER(value_struct)

        self.h_map_object = windll.kernel32.OpenFileMappingW(
            FILE_MAP_ALL_ACCESS, False, name)

        if create and not self.h_map_object:
            self.h_map_object = windll.kernel32.CreateFileMappingW(
                INVALID_HANDLE_VALUE, None, PAGE_READ_WRITE, 0, size, name)

        if not self.h_map_object:
            raise Exception("Unable to open shared memory")

        self.pointer = windll.kernel32.MapViewOfFile(
            self.h_map_object, FILE_MAP_ALL_ACCESS, 0, 0, size)

        self.value = cast(self.pointer, pointer_type)

    def __del__(self):
        self.close()

    def close(self):
        if self.pointer:
            windll.kernel32.UnmapViewOfFile(self.pointer)
            self.pointer = None

        if self.h_map_object:
            windll.kernel32.CloseHandle(self.h_map_object)
            self.h_map_object = None

    def __getattr__(self, item):
        return getattr(self.value.contents, item)


class GuildWars2FileMapping(FileMapping):
    def __init__(self, name=u"MumbleLink", value_struct=LinkedMem,
                 create=True):
        super(GuildWars2FileMapping, self).__init__(name, value_struct, create)

    def get_map(self, lang="en"):
        return maps(self.context.mapId, lang)

    def get_map_location(self):
        """Get the location of the player, converted to world coordinates.

        :return: a tuple (x, y, z).

        """
        map_data = self.get_map()
        (bounds_e, bounds_n), (bounds_w, bounds_s) = map_data["continent_rect"]
        (map_e, map_n), (map_w, map_s) = map_data["map_rect"]

        assert bounds_w < bounds_e
        assert bounds_n < bounds_s
        assert map_w < map_e
        assert map_n < map_s

        meters_to_inches = 39.3701
        x, y, z = self.fAvatarPosition

        map_x = bounds_w + ((x * meters_to_inches - map_w) /
                            (map_e - map_w) * (bounds_e - bounds_w))
        map_y = bounds_n + ((-z * meters_to_inches - map_n) /
                            (map_s - map_n) * (bounds_s - bounds_n))
        map_z = y * meters_to_inches

        return map_x, map_y, map_z


gw2link = GuildWars2FileMapping()
