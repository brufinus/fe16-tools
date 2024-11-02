"""Provide utility functions for the tools blueprint.

This module contains utility functions that provide common functionality to tool view functions.

Functions:
    - get_choices: Return a list of choices from a table.
    - get_yield_ratios: Return additional values from a greenhouse score.
"""


def get_choices(table, sort):
    """Return a list of id and name tuples from a database table.

    This function is used to populate form dropdowns.

    :param table: The database table to query. The table must have an id and name column.
    :type table: Model
    :param sort: Sort the returned list by name.
    :type sort: bool
    :return: The list of id, name tuples.
    :rtype: list[tuple[int, str]]
    """

    result_list = []
    if sort:
        rows = table.query.order_by(table.name.asc()).all()
    else:
        rows = table.query.all()
    for row in rows:
        tup = (row.id, row.name)
        result_list.append(tup)
    return result_list


def get_yield_ratios(score):
    """Return the yield, ratio, and stat-booster coefficient over a score range.

    This function is used for the seed simulator tool.

    :param score: The hidden greenhouse score.
    :type score: int
    :return: The associated yield, ratio, and stat-booster coefficient.
    :rtype: tuple[int, str, int]
    """

    ranges = [
        (1, 0, "", 0),
        (21, 1, "7:3", 1),
        (41, 1, "2:8", 3),
        (61, 2, "7:3", 5),
        (81, 2, "4:6", 10),
        (91, 3, "8:2", 15),
        (101, 4, "3:7", 20),
    ]

    for limit, yld, ratio, coefficient in ranges:
        if score < limit:
            return yld, ratio, coefficient
