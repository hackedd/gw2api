import os
import time
import json
from struct import pack, unpack
from base64 import b64encode, b64decode

import gw2api


__all__ = ("encode_item_link", "encode_coin_link",
           "encode_chat_link", "decode_chat_link")


def mtime(path):
    """Get the modification time of a file, or -1 if the file does not exist.
    """
    if not os.path.exists(path):
        return -1
    stat = os.stat(path)
    return stat.st_mtime


def get_cached(path, cache_name=None, **kwargs):
    """Request a resource form the API, first checking if there is a cached
    response available. Returns the parsed JSON data.
    """
    if gw2api.cache_dir and gw2api.cache_time and cache_name is not False:
        if cache_name is None:
            cache_name = path
        cache_file = os.path.join(gw2api.cache_dir, cache_name)
        if mtime(cache_file) >= time.time() - gw2api.cache_time:
            with open(cache_file, "r") as fp:
                return json.load(fp)
    else:
        cache_file = None

    r = gw2api.session.get(gw2api.BASE_URL + path, **kwargs)

    if not r.ok:
        try:
            response = r.json()
        except ValueError:  # pragma: no cover
            response = None
        if isinstance(response, dict) and "text" in response:
            r.reason = response["text"]

    r.raise_for_status()
    data = r.json()

    if cache_file:
        with open(cache_file, "w") as fp:
            json.dump(data, fp, indent=2)

    return data


def encode_item_link(item_id, number=1, skin_id=None,
                     upgrade1=None, upgrade2=None):
    """Encode a chat link for an item (or a stack of items).

    :param item_id: the Id of the item
    :param number: the number of items in the stack
    :param skin_id: the id of the skin applied to the item
    :param upgrade1: the id of the first upgrade component
    :param upgrade2: the id of the second upgrade component
    """
    return encode_chat_link(gw2api.TYPE_ITEM, id=item_id, number=number,
                            skin_id=skin_id, upgrade1=upgrade1,
                            upgrade2=upgrade2)


def encode_coin_link(copper, silver=0, gold=0):
    """Encode a chat link for an amount of coins.
    """
    return encode_chat_link(gw2api.TYPE_COIN, copper=copper, silver=silver,
                            gold=gold)


def encode_chat_link(link_type, **kwargs):
    if link_type in gw2api.LINK_TYPES:
        link_type = gw2api.LINK_TYPES[link_type]

    if link_type == gw2api.TYPE_COIN:
        if "copper" in kwargs or "silver" in kwargs or "gold" in kwargs:
            amount = (kwargs.get("gold", 0) * 100 * 100 +
                      kwargs.get("silver", 0) * 100 +
                      kwargs.get("copper", 0))
        else:
            amount = kwargs["amount"]
        data = pack("<BI", link_type, amount)

    elif link_type == gw2api.TYPE_ITEM:
        item_id = kwargs["id"]

        args = []
        for i, key in enumerate(("skin_id", "upgrade1", "upgrade2")):
            value = kwargs.get(key)
            if value:
                item_id |= 2 << (28 + i)
                args.append(value)

        format = "<BBI" + "I" * len(args)
        data = pack(format, link_type, kwargs.get("number", 1), item_id, *args)

    elif link_type in (gw2api.TYPE_TEXT, gw2api.TYPE_MAP, gw2api.TYPE_SKILL,
                       gw2api.TYPE_TRAIT, gw2api.TYPE_RECIPE,
                       gw2api.TYPE_SKIN, gw2api.TYPE_OUTFIT):
        data = pack("<BI", link_type, kwargs["id"])

    elif isinstance(link_type, int):
        raise Exception("Unknown link type 0x%02x" % link_type)

    else:
        raise Exception("Unknown link type '%s'" % link_type)

    return "[&%s]" % b64encode(data).decode("ascii")


def decode_chat_link(string):
    if string.startswith("[&") and string.endswith("]"):
        string = string[2:-1]

    data = b64decode(string.encode("ascii"))

    link_type, = unpack("<B", data[:1])

    if link_type == gw2api.TYPE_COIN:
        amount, = unpack("<I", data[1:])
        return "coin", {"amount": amount}

    if link_type == gw2api.TYPE_ITEM:
        number, item_id = unpack("<BI", data[1:6])
        flags = (item_id & 0xFF000000) >> 24
        item_id &= 0x00FFFFFF
        values = {"number": number, "id": item_id}
        o = 6
        if flags & 0x80:
            values["skin_id"], = unpack("<I", data[o:o+4])
            o += 4
        if flags & 0x40:
            values["upgrade1"], = unpack("<I", data[o:o+4])
            o += 4
        if flags & 0x20:
            values["upgrade2"], = unpack("<I", data[o:o+4])
            o += 4
        return "item", values

    link_type_string = None
    for key, value in gw2api.LINK_TYPES.items():
        if value == link_type:
            link_type_string = key

    if link_type in (gw2api.TYPE_TEXT, gw2api.TYPE_MAP, gw2api.TYPE_SKILL,
                     gw2api.TYPE_TRAIT, gw2api.TYPE_RECIPE,
                     gw2api.TYPE_SKIN, gw2api.TYPE_OUTFIT):
        id, = unpack("<I", data[1:])
        return link_type_string, {"id": id}

    raise Exception("Unknown link type 0x%02x" % link_type)
