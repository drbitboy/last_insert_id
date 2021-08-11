## Purpose

Demonstrate manual method to obtain LAST_INSERT_ID() from MySQL server on a database e.g. when provided API (AVEVA/Indusoft) does not work with MySQL correctly and LAST_INSERT_ID() cannot be used

Cf. https://www.plctalk.net/qanda/showthread.php?t=130178

## Usage

    python last_insert_id.py [row_value]

## Typical output

    Created database test_forty2
    {'bad_last_insert_id': 0,
     'last_insert_id': '1',
     'manual_last_insert_id': 1,
     'value_added': '0.172'}

    row_id	forty2_col
    1	0.172


    {'bad_last_insert_id': 0,
     'last_insert_id': '2',
     'manual_last_insert_id': 2,
     'value_added': '-0.30'}

    row_id	forty2_col
    1	0.172
    2	-0.30


    {'bad_last_insert_id': 0,
     'last_insert_id': '3',
     'manual_last_insert_id': 3,
     'value_added': '-0.86'}

    row_id	forty2_col
    1	0.172
    2	-0.30
    3	-0.86

