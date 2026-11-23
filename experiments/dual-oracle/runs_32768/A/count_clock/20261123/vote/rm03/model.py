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
            reset = row[0]
            ena = row[1]
        if reset:
            hh, mm, ss, pm = 12, 0, 0, 0
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
            'hh': ((hh // 10) << 4) | (hh % 10),
            'mm': ((mm // 10) << 4) | (mm % 10),
            'ss': ((ss // 10) << 4) | (ss % 10)
        })
    return out
