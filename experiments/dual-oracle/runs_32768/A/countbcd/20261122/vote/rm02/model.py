def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        r = row.get('reset', 0) if isinstance(row, dict) else row[0]
        if r:
            q = 0
        else:
            o = q & 15
            t = (q >> 4) & 15
            h = (q >> 8) & 15
            th = (q >> 12) & 15
            o += 1
            if o == 10:
                o = 0
                t += 1
                if t == 10:
                    t = 0
                    h += 1
                    if h == 10:
                        h = 0
                        th = (th + 1) % 10
            q = (th << 12) | (h << 8) | (t << 4) | o
        o = q & 15
        t = (q >> 4) & 15
        h = (q >> 8) & 15
        e1 = 1 if o == 9 else 0
        e2 = 1 if (o == 9 and t == 9) else 0
        e3 = 1 if (o == 9 and t == 9 and h == 9) else 0
        out.append({'ena': e1 | (e2 << 1) | (e3 << 2), 'q': q})
    return out
