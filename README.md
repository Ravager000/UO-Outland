# UO-Outland
## ClassicUO Razor
### Collection of usefull script & tools

Vendor Data.py     **Output Sample**

journal_processed.txt
--------------------------------------------------
Vendor: Pale Dim's Butler (ID: 1703153)
Location: (3713, 3466, 69) 161° 53'S, 168° 2'E

Inventory:
  - Item ID: 1393435505, Description: Shadow Aspect Core, Amount: 1, Stack Price: 41000
  - Item ID: 1393302192, Description: Command Aspect Core, Amount: 1, Stack Price: 40000
  - Item ID: 1116694652, Description: mount gear dye (hue 2828: metallic pickle), Amount: 1, Stack Price: 2222
  - Item ID: 1225629804, Description: mount gear dye (hue 1465: dark blood), Amount: 1, Stack Price: 2222
  - Item ID: 1213479720, Description: mount gear dye (hue 1182: wilderness), Amount: 2, Stack Price: 2222
  - Item ID: 1081553974, Description: mount gear dye (hue 1995: metallic wine), Amount: 1, Stack Price: 2222
  - Item ID: 1403288244, Description: mount gear dye (hue 2167: metallic pewter), Amount: 1, Stack Price: 2222
  - Item ID: 1395282129, Description: alchemy skill mastery scroll, Amount: 2, Price: 120000
  - Item ID: 1103796835, Description: very rare seed, Amount: 2, Price: 8000
  - Item ID: 1395937782, Description: pristine lumber, Amount: 1, Price: 35000
  - Item ID: 1395939336, Description: immaculate stone, Amount: 2, Price: 80000
  - Item ID: 1166095673, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
  - Item ID: 1166095668, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
  - Item ID: 1166095672, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
  - Item ID: 1166095671, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
  - Item ID: 1166095669, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
  - Item ID: 1166095667, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
  - Item ID: 1166095670, Description: bronze mastery chain link Time Dungeon Damage (+2.00%), Amount: 1, Price: 85000
--------------------------------------------------



journal_inventory_summary.txt

====================== Inventory Summary ======================

- Item Description: water phylactery, Total Amount: 1, Prices: [99999], Average Unit Price: 99999.0, Total Value: 99999
- Item Description: backpack dye (hue 2255: powder lapis), Total Amount: 1, Prices: [69998], Average Unit Price: 69998.0, Total Value: 69998
- Item Description: Blood Aspect Core, Total Amount: 2, Prices: [20000, 18500], Average Unit Price: 19250.0, Total Value: 38500
- Item Description: rosewood lumber map (undeciphered), Total Amount: 2, Prices: [2000, 2300], Average Unit Price: 2150.0, Total Value: 4300
- Item Description: Inferno (collectable card), Total Amount: 1, Prices: [4000], Average Unit Price: 4000.0, Total Value: 4000
- Item Description: Lodestone (collectable card), Total Amount: 1, Prices: [3000], Average Unit Price: 3000.0, Total Value: 3000
- Item Description: bronze mastery chain link Chivalry Skill (+2.50), Total Amount: 1, Prices: [95000], Average Unit Price: 95000.0, Total Value: 95000
- Item Description: silver mastery chain link Necromancy Skill (+3.12), Total Amount: 1, Prices: [700000], Average Unit Price: 700000.0, Total Value: 700000
- Item Description: bronze mastery chain link Darkmire Temple Damage (+2.00%), Total Amount: 8, Prices: [95000, 74000], Average Unit Price: 84500.0, Total Value: 739000
- Item Description: bronze mastery chain link Damage Dealt By Player (+1.25%), Total Amount: 4, Prices: [95000], Average Unit Price: 95000.0, Total Value: 380000 

Overall Total Value: 201433

===============================================================

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