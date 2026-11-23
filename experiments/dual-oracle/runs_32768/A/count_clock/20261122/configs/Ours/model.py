def reference(vectors):
    h = 12
    m = 0
    s = 0
    pm = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        en = v.get('ena', 0)
        if r:
            h = 12
            m = 0
            s = 0
            pm = 0
        elif en:
            s += 1
            if s == 60:
                s = 0
                m += 1
                if m == 60:
                    m = 0
                    if h == 12:
                        h = 1
                    elif h == 11:
                        h = 12
                        pm ^= 1
                    else:
                        h += 1
        out.append({
            'pm': pm,
            'hh': ((h // 10) << 4) | (h % 10),
            'mm': ((m // 10) << 4) | (m % 10),
            'ss': ((s // 10) << 4) | (s % 10)
        })
    return out
