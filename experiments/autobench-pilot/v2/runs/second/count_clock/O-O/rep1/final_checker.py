def reference(vectors):
    hh = 12
    mm = 0
    ss = 0
    pm = 0
    out = []
    for v in vectors:
        if v.get('reset'):
            hh, mm, ss, pm = 12, 0, 0, 0
        elif v.get('ena'):
            ss += 1
            if ss == 60:
                ss = 0
                mm += 1
                if mm == 60:
                    mm = 0
                    hh += 1
                    if hh == 13:
                        hh = 1
                    if hh == 12:
                        pm ^= 1
        out.append({
            'pm': pm,
            'hh': ((hh // 10) << 4) | (hh % 10),
            'mm': ((mm // 10) << 4) | (mm % 10),
            'ss': ((ss // 10) << 4) | (ss % 10),
        })
    return out
