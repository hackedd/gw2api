****************
Guild Wars 2 API
****************

gw2api is a Python library to interface with the `Guild Wars 2 API`_. It aims
to have an almost one-to-one mapping to the JSON API, with only some minor
differences.

Usage Example
-------------

.. code-block:: python

    #!/usr/bin/env python
    import gw2api

    for item_id in range(30684, 30705):
        details = gw2api.item_details(item_id)
        link = gw2api.encode_item_link(item_id)
        print "%-26s %-9s %-10s %s" % (details["name"], details["rarity"],
                                       details["weapon"]["type"], link)

gw2api is available from the `Python Package Index`_ and is hosted on GitHub_.

.. _Guild Wars 2 API: http://wiki.guildwars2.com/wiki/API:Main
.. _Python Package Index: https://pypi.python.org/pypi/gw2api
.. _GitHub: https://github.com/hackedd/gw2api
