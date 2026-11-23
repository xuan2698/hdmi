def reference(vectors):
    hour = 12
    minute = 0
    second = 0
    pm = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            ena = row.get('ena', 0)
        else:
            reset = row[0] if len(row) > 0 else 0
            ena = row[1] if len(row) > 1 else 0
        reset = int(reset) & 1
        ena = int(ena) & 1
        if reset:
            hour = 12
            minute = 0
            second = 0
            pm = 0
        elif ena:
            second += 1
            if second == 60:
                second = 0
                minute += 1
                if minute == 60:
                    minute = 0
                    hour += 1
                    if hour == 12:
                        pm ^= 1
                    elif hour == 13:
                        hour = 1
        out.append({
            'pm': pm,
            'hh': (hour // 10) * 16 + (hour % 10),
            'mm': (minute // 10) * 16 + (minute % 10),
            'ss': (second // 10) * 16 + (second % 10)
        })
    return out
