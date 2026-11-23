def reference(vectors):
    h = 12
    m = 0
    s = 0
    pm = 0
    out = []
    for r in vectors:
        if isinstance(r, dict):
            rst = r.get('reset', 0)
            ena = r.get('ena', 0)
        elif isinstance(r, int):
            rst = (r >> 1) & 1
            ena = r & 1
        else:
            rst = r[0]
            ena = r[1] if len(r) > 1 else 0
        if rst:
            h, m, s, pm = 12, 0, 0, 0
        elif ena:
            s += 1
            if s == 60:
                s = 0
                m += 1
                if m == 60:
                    m = 0
                    if h == 11:
                        h = 12
                        pm ^= 1
                    elif h == 12:
                        h = 1
                    else:
                        h += 1
        out.append({
            'pm': pm,
            'hh': ((h // 10) << 4) | (h % 10),
            'mm': ((m // 10) << 4) | (m % 10),
            'ss': ((s // 10) << 4) | (s % 10)
        })
    return out
