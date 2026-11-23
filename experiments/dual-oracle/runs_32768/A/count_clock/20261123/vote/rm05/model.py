def reference(vectors):
    total = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            ena = row.get('ena', 0)
        else:
            reset = row[0]
            ena = row[1]

        if reset:
            total = 0
        elif ena:
            total = (total + 1) % 86400

        h24 = total // 3600
        pm = 1 if h24 >= 12 else 0

        hour = h24 % 12
        if hour == 0:
            hour = 12

        minute = (total // 60) % 60
        second = total % 60

        hh = ((hour // 10) << 4) | (hour % 10)
        mm = ((minute // 10) << 4) | (minute % 10)
        ss = ((second // 10) << 4) | (second % 10)

        result.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})

    return result
