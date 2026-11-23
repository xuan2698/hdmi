def reference(vectors):
    h = 12
    m = 0
    s = 0
    pm = 0
    out = []
    for v in vectors:
        if v['reset']:
            h = 12
            m = 0
            s = 0
            pm = 0
        elif v['ena']:
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
        hh = ((h // 10) << 4) | (h % 10)
        mm = ((m // 10) << 4) | (m % 10)
        ss = ((s // 10) << 4) | (s % 10)
        out.append({'pm': pm, 'hh': hh, 'mm': mm, 'ss': ss})
    return out
