# UO-Outland
## ClassicUO Razor
### Collection of usefull script & tools

Loot Inventory Data.py     **Output Sample**

journal_Items.txt

Processed Data from 2025_03_09_23_41_54_journal
Date: 2025-03-10 03:25:06

====================== Inventory Summary ======================
Found 13 total items, merged into 10 unique items.

(ID: 1139692141)  unidentified magic spellbook, Amount: 4
(ID: 1140310936)  citrine , Amount: 4
(ID: 1139881832)  sapphire , Amount: 2
(ID: 1139694215)  tourmaline , Amount: 2
(ID: 1139591302)  leather , Amount: 774
(ID: 1140081213)  rosehide , Amount: 85
(ID: 1140122189)  unidentified platemail gorget, Amount: 1
(ID: 1140310937)  shadowhide skinning map (undeciphered), Amount: 1
(ID: 1139694216)  plant chemicals, Amount: 1
(ID: 9999999999)  gold, Amount: 8644

===============================================================

Vendor Data.py     **Output Sample**

journal_processed.txt
--------------------------------------------------
Vendor: [10% discount for LDS] Mr.Freeze (ID: 4460921)
Location: (3713, 3470, 69) 162° 14'S, 168° 2'E
Inventory:
  No items listed
--------------------------------------------------
Vendor: Pale Dim's Butler (ID: 1703153)
Location: (3713, 3470, 69) 162° 14'S, 168° 2'E
Inventory:
  - Item (ID: 1101085410) carpet dye (hue 2093: shadowspire cathedral), Amount: 1, Stack Price: 50000
  - Item (ID: 1362482556) silver mastery chain link Follower Damage (+2.50%), Amount: 1, Price: 750000
  - Item (ID: 1930491237) eldritch phylactery, Amount: 1, Stack Price: 5000
  - Item (ID: 1888544012) shadow phylactery, Amount: 1, Stack Price: 8000
  - Item (ID: 1136918996) begging skill mastery scroll, Amount: 2, Stack Price: 6500
--------------------------------------------------

journal_inventory_summary.txt

====================== Inventory Summary ======================

- Item herding skill mastery scroll, Total Amount: 8, Prices: [18000], Average Price: 18000.0, Total Value: 144000
- Item spirit speak skill mastery scroll, Total Amount: 8, Prices: [19000], Average Price: 19000.0, Total Value: 152000
- Item rare cloth (hue 1156: dark blueberry), Total Amount: 2, Prices: [5000], Average Price: 5000.0, Total Value: 10000
- Item cleansing brew, Total Amount: 1500, Prices: [875], Average Price: 875.0, Total Value: 1312500
- Item water phylactery, Total Amount: 1, Prices: [99999], Average Price: 99999.0, Total Value: 99999
- Item backpack dye (hue 2255: powder lapis), Total Amount: 1, Prices: [69998], Average Price: 69998.0, Total Value: 69998
- Item Blood Aspect Core, Total Amount: 2, Prices: [20000, 18500], Average Price: 19250.0, Total Value: 38500
- Item bronze mastery chain link Damage to Poisoned Creatures (+1.75%), Total Amount: 1, Prices: [95000], Average Price: 95000.0, Total Value: 95000
- Item bronze mastery chain link Damage to Undead Creatures (+2.50%), Total Amount: 1, Prices: [100500], Average Price: 100500.0, Total Value: 100500

Overall Total Value: 201433

===============================================================

journal_changes.txt

=== Vendor Comparison Results ===

Added Vendors:
  - Case's Bazaar (ID: 4467716)
    Location: (3713, 3470, 69) 162° 14'S, 168° 2'E
    Items:
      - (ID: 1205194016) dark crimson cloth boots (hue 1939), Amount: 1, Price: 60000
      - (ID: 1148354549) Quaeven painting (portrait painting antiquity), Amount: 1, Price: 150000

Item Changes:

  Vendor ID: 1191061
    Added Items:
      - (ID: 1328094155) cleansing brew, Amount: 1500, Stack Price: 875

  Vendor ID: 6145079
    Removed Items:
      - (ID: 1318008344) rosewood lumber map (undeciphered), Amount: 1, Price: 2000
      - (ID: 1889585983) bronze mastery chain link Chivalry Skill (+2.50), Amount: 1, Price: 95000

 Changed Items:
      - Item ID: 1397722479
        Old: sentry outfitting ship upgrade (5,000 base doubloon cost), Amount: 1, Price: 130000
        New: sentry outfitting ship upgrade (5,000 base doubloon cost), Amount: 1, Price: 115000
      - Item ID: 1397679375
        Old: flesh iron cannon metal ship upgrade (2,500 base doubloon cost), Amount: 1, Price: 170000
        New: flesh iron cannon metal ship upgrade (2,500 base doubloon cost), Amount: 1, Price: 150000
      - Item ID: 1405415146
        Old: limes crew supplies ship upgrade (2,500 base doubloon cost), Amount: 1, Price: 80000
        New: limes crew supplies ship upgrade (2,500 base doubloon cost), Amount: 1, Price: 60000

++++++++++++++++++++++++++++++++++++++++++++++++++

journal_changes.json

"4035411": {
            "added_items": [
                {
                    "id": "1327204412",
                    "price": "2950000",
                    "description": "gold mastery chain link Pulma Damage (+3.00%)",
                    "amount": "1"
                }
            ],
            "removed_items": [
                {
                    "id": "1087145771",
                    "price": "15000",
                    "description": "dull copper ore map (undeciphered)",
                    "amount": "1"
                },
                {
                    "id": "1421791774",
                    "price": "5000",
                    "description": "eminently accurate greater undead slaying druid staff",
                    "amount": "1"
                }
            ],
            "changed_items": [
                {
                    "item_id": "1085054953",
                    "old": {
                        "id": "1085054953",
                        "price": "2000",
                        "description": "bronzewood lumber map (undeciphered)",
                        "amount": "1"
                    },
                    "new": {
                        "id": "1085054953",
                        "price": "1300",
                        "description": "bronzewood lumber map (undeciphered)",
                        "amount": "1"
                    }
                },
                {
                    "item_id": "1088868848",
                    "old": {
                        "id": "1088868848",
                        "price": "5500",
                        "description": "verescale fishing map (undeciphered)",
                        "amount": "1"
                    },
                    "new": {
                        "id": "1088868848",
                        "price": "5000",
                        "description": "verescale fishing map (undeciphered)",
                        "amount": "1"
                    }
                }
            ]
        },

++++++++++++++++++++++++++++++++++++++++++++++++++

journal_inventory_summary.json
{
    "inventory": {
        "flesh iron cannon metal ship upgrade (2,500 base doubloon cost)": {
            "amount": 1,
            "prices": [
                170000
            ],
            "total_value": 170000,
            "avg_unit_price": 170000.0
        },
        "alchemy skill mastery scroll": {
            "amount": 4,
            "prices": [
                60000,
                52500
            ],
            "total_value": 225000,
            "avg_unit_price": 56250.0
        },
                "leather": {
            "amount": 15,
            "prices": [
                666
            ],
            "total_value": 9990,
            "avg_unit_price": 666.0
        }
    },
    "total_value": 20143326
}

++++++++++++++++++++++++++++++++++++++++++++++++++

journal_processed.json
{
        "id": "3588345",
        "name": "Dee",
        "location": "(3714, 3470, 69) 162° 14'S, 168° 7'E",
        "items": [
            {
                "id": "1397679375",
                "price": "170000",
                "description": "flesh iron cannon metal ship upgrade (2,500 base doubloon cost)",
                "amount": "1"
            },
            {
                "id": "1397722479",
                "price": "130000",
                "description": "sentry outfitting ship upgrade (5,000 base doubloon cost)",
                "amount": "1"
            },
            {
                "id": "1115214261",
                "stack_price": "5000",
                "description": "rare cloth (hue 1939: dark crimson)",
                "amount": "2"
            },
            {
                "id": "1231491190",
                "stack_price": "18000",
                "description": "herding skill mastery scroll",
                "amount": "8"
            },
         ]
    },