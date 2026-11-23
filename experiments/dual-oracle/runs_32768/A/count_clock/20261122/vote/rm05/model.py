def reference(vectors):
    h, m, s, pm = 12, 0, 0, 0
    out = []
    for v in vectors:
        if isinstance(v, dict):
            reset = v.get('reset', 0)
            ena = v.get('ena', 0)
        else:
            reset = v[0] if len(v) > 0 else 0
            ena = v[1] if len(v) > 1 else 0
        reset = 1 if reset else 0
        ena = 1 if ena else 0

        if reset:
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
                        pm = 1 - pm
                    elif h == 12:
                        h = 1
                    else:
                        h += 1

        out.append({
            'pm': pm,
            'hh': (h // 10) * 16 + (h % 10),
            'mm': (m // 10) * 16 + (m % 10),
            'ss': (s // 10) * 16 + (s % 10)
        })
    return out
