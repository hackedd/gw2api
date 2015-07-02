****************
Guild Wars 2 API
****************

gw2api is a Python library to interface with the `Guild Wars 2 API`_. It aims
to have an almost one-to-one mapping to the JSON API, with only some minor
differences.

Usage Example
-------------

.. code-block:: python

    import gw2api.v2

    for item in gw2api.v2.items.get(range(30684, 30705)):
        link = gw2api.encode_item_link(item["id"])
        print "%-26s %-9s %-10s %s" % (item["name"], item["rarity"],
                                       item["details"]["type"], link)

gw2api is available from the `Python Package Index`_ and is hosted on GitHub_.

.. _Guild Wars 2 API: http://wiki.guildwars2.com/wiki/API:Main
.. _Python Package Index: https://pypi.python.org/pypi/gw2api
.. _GitHub: https://github.com/hackedd/gw2api
