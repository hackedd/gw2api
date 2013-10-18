Item Properties
===============

In general, all items contain a property with details which are specific to
the particular type of item. For example, weapons contain information about
their damage range, while bags contain information about the number of slots.

Weapons
-------

type (string):
    .. _weapon types:

    The type of weapon. One of: ``Axe``, ``Dagger``, ``Focus``,
    ``Greatsword``, ``Hammer``, ``Harpoon``, ``LongBow``, ``Mace``,
    ``Pistol``, ``Rifle``, ``Scepter``, ``Shield``, ``ShortBow``,
    ``Speargun``, ``Staff``, ``Sword``, ``Torch``, ``Trident`` or ``Warhorn``.

min_power (integer):
    The lower bound of the displayed weapon strength.

max_power (integer):
    The upper bound of the displayed weapon strength.

defense (integer):
    The defense of the weapon (only applies to shields).

damage_type (string):
    The damage type done by the weapon. Usually ``Physical``, but there are
    some weapons inflicting ``Fire``, ``Lightning`` or ``Ice`` damage.

infusion_slots (list):
    .. _infusion_slots:

    Contains a list with the infusion slots (if the weapon has any). Each
    item in the list is an object detailing one infusion slot. The item has
    a list of flags detailing the type of slot. For example, the ascended
    `Mathilde's Harpoon Gun`_ has two offensive infusion slots::

        "infusion_slots": [
          {
            "flags": [
              "Offense"
            ]
          },
          {
            "flags": [
              "Offense"
            ]
          }
        ]

    .. _Mathilde's Harpoon Gun:
       http://wiki.guildwars2.com/wiki/Mathilde%27s_Harpoon_Gun

infix_upgrade (optional):
    .. _infix_upgrade:

    This property has two optional attributes, which together describe the
    base attributes of the weapon.

    attributes (list):
        A list of ``attribute`` and ``modifier`` pairs.

    buff:
        Contains a ``skill_id`` and ``description``.

    For example, the Giver's `Iron Axe`_ contains the following::

        "infix_upgrade": {
          "buff": {
            "description": "+10% Condition Duration",
            "skill_id": "16631"
          },
          "attributes": [
            {
              "modifier": "17",
              "attribute": "Vitality"
            }
          ]
        },

    Giving the item +10% Condition Duration and +17 Vitality.

    .. _Iron Axe:
       http://wiki.guildwars2.com/wiki/Iron_Axe

Armor
-----

type (string):
    The type of armor. ``Boots``, ``Coat``, ``Gloves``, ``Helm``,
    ``HelmAquatic``, ``Leggings`` or ``Shoulders``

weight_class (string):
    Weight class. ``Light``, ``Medium`` or ``Heavy`` for normal armor,
    ``Clothing`` for town clothes.

defense (integer):
    The defense rating of the armor piece.

suffix_item_id (integer):
    The item Id of the particular upgrade component that has been applied to
    this armor piece.

infusion_slots (list):
    Probably follows the same format as the infusion_slots_ attribute for
    weapons. However, as of 15-10-2013 there are not yet any ascended armor pieces, so unable to verify.

infix_upgrade (optional):
    See the infix_upgrade_ attribute on weapons.

Back Items
----------

The specific item property for Back items is ``back``. It shares most of its
attributes with Trinkets, but has no subtypes.

suffix_item_id:
    The item Id of the particular upgrade component that has been applied to
    this Trinket.

infusion_slots:
    See the infusion_slots_ attribute on weapons.

infix_upgrade:
    See the infix_upgrade_ attribute on weapons.

Trinkets
--------

type (string):
    The type of Trinket. One of ``Accessory``, ``Amulet`` or ``Ring``.

suffix_item_id (integer):
    The item Id of the particular upgrade component that has been applied to
    this Trinket.

infusion_slots:
    See the infusion_slots_ attribute on weapons.

infix_upgrade:
    See the infix_upgrade_ attribute on weapons.


Consumables
-----------

type (string):
    The type of consumable. One of ``AppearanceChange``, ``Booze``,
    ``ContractNpc``, ``Food``, ``Generic``, ``Halloween``, ``Immediate``,
    ``Transmutation``, ``Unknown``, ``Unlock`` or ``Utility``.

unlock_type (string; optional):
    If ``type`` is ``Unlock``; ``unlock_type`` will be one of ``BagSlot``,
    ``BankTab``, ``CraftingRecipe``, ``Dye`` or ``Unknown``

description:
    Description of the consumable.

recipe_id (integer; optional):
    If ``unlock_type`` is ``CraftingRecipe``; contains the Id of the recipe
    that is unlocked by this recipe sheet.

duration_ms (integer):
    The duration, in milliseconds, of the buffs applied by the consumable.
    Usually applies to consumables of type ``Food`` or ``Utility``, but is
    also set for some other consumables.

color_id (integer):
    If ``unlock_type`` is ``Dye``, contains the Id of the color that is
    unlocked by this dye.

Upgrade Components
------------------

The specific item property for Upgrade Components is ``upgrade_component``.

type (string):
    Upgrade component type. One of ``Default``, ``Gem``, ``Rune``, or
    ``Sigil``. Infusions and jewels have their type set to ``Default``. The
    other upgrade components with type ``Default`` seem to be PvP versions of
    upgrade components (for example: `Superior Rune of Strength`_ and `Superior Rune of Strength (PvP)`_).

   .. _Superior Rune of Strength:
      https://api.guildwars2.com/v1/item_details.json?item_id=24714

   .. _Superior Rune of Strength (PvP):
      https://api.guildwars2.com/v1/item_details.json?item_id=21092

suffix (string):
    The specific suffix_ for the upgrade component.

    .. _suffix:
       http://wiki.guildwars2.com/wiki/Item_nomenclature

infusion_upgrade_flags (list):
    For infusions, the type of infusion. One or more of ``Defense``,
    ``Offense`` and ``Utility``.

infix_upgrade:
    See the infix_upgrade_ attribute on weapons. However, the ``attributes``
    are always empty, only the ``buff`` is ever filled. Only applies to PvP
    Sigils.

flags (list):
    The types of equipment this upgrade can be applied to. Can be any of the
    `weapon types`_, ``LightArmor``, ``MediumArmor``, ``HeavyArmor`` and
    ``Trinket``.

bonuses (list):
    A list of strings describing the bonuses given by the upgrade component.
    Applies to Runes and PvP Runes.

Bags
----

size (integer):
    The number of slots the bag has.

no_sell_or_sort (integer):
    Set to ``1`` for Invisable Bags and Safe Boxes (for which the contents
    will never appear in a sell-to-vendor list and will not move when
    inventory is sorted). ``0`` for all other bag types.

Containers
----------

Containers have one extra attribute, ``type`` whis is usually ``Default``.
The only other observed value is ``GiftBox``.

Gizmos
------

Gizmos have one extra attribute, ``type`` whis is usually ``Default``. Other
observed values are ``RentableContractNpc`` and ``UnlimitedConsumable``.

Gathering Tools
---------------

The specific item property for Gathering tools is ``gathering``. It contains
only one attribute, ``type``, which can be ``Foraging`` (for Harvesting
Sickles), ``Logging`` or ``Mining``.

Salvage Kits
------------

The specific item property for Salvage kits is ``tool``. It contains the
attributes ``type`` (which is always ``Salvage``) and ``charges`` which is the
number of uses of the kit.
