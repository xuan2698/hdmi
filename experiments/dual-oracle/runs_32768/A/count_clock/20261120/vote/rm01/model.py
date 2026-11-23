def reference(vectors):
    hh = 12
    mm = 0
    ss = 0
    pm = 0
    out = []
    for row in vectors:
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            ena = row.get('ena', 0)
        else:
            reset = row[0] if len(row) > 0 else 0
            ena = row[1] if len(row) > 1 else 0

        if reset:
            hh = 12
            mm = 0
            ss = 0
            pm = 0
        elif ena:
            ss += 1
            if ss == 60:
                ss = 0
                mm += 1
                if mm == 60:
                    mm = 0
                    if hh == 11:
                        hh = 12
                        pm ^= 1
                    elif hh == 12:
                        hh = 1
                    else:
                        hh += 1

        out.append({
            'pm': pm,
            'hh': (hh // 10) * 16 + (hh % 10),
            'mm': (mm // 10) * 16 + (mm % 10),
            'ss': (ss // 10) * 16 + (ss % 10),
        })
    return out
