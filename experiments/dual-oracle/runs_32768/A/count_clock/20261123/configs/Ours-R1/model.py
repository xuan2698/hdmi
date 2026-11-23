def reference(vectors):
    h = 12
    m = 0
    s = 0
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
            h = 12
            m = 0
            s = 0
            pm = 0
        elif ena:
            s += 1
            if s >= 60:
                s = 0
                m += 1
                if m >= 60:
                    m = 0
                    h += 1
                    if h == 13:
                        h = 1
                    if h == 12:
                        pm ^= 1
        hh = ((h // 10) << 4) | (h % 10)
        mm = ((m // 10) << 4) | (m % 10)
        ss = ((s // 10) << 4) | (s % 10)
        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})
    return out
