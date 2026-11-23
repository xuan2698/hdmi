def reference(vectors):
    idx = 0      # minute index within 12-hour cycle: 0=12:00, 60=01:00, ..., 660=11:00
    sec = 0      # seconds 0..59
    pm = 0       # 0=AM, 1=PM
    result = []

    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            ena = row.get('ena', 0)
        else:
            reset = row[0]
            ena = row[1]

        if reset:
            idx = 0
            sec = 0
            pm = 0
        elif ena:
            sec += 1
            if sec == 60:
                sec = 0
                idx += 1
                if idx == 720:
                    idx = 0
                    pm ^= 1

        hour = idx // 60
        if hour == 0:
            hour = 12
        minute = idx % 60

        hh = ((hour // 10) << 4) | (hour % 10)
        mm = ((minute // 10) << 4) | (minute % 10)
        ss = ((sec // 10) << 4) | (sec % 10)

        result.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})

    return result
