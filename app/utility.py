def get_choices(table, sort):
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
