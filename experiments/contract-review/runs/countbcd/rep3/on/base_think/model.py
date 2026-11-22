def reference(vectors):
    q = 0
    cur_reset = 0
    out = []
    for row in vectors:
        if 'reset' in row:
            cur_reset = row['reset']
        if cur_reset:
            d0 = d1 = d2 = d3 = 0
        else:
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15
            d0 += 1
            if d0 == 10:
                d0 = 0
                d1 += 1
                if d1 == 10:
                    d1 = 0
                    d2 += 1
                    if d2 == 10:
                        d2 = 0
                        d3 += 1
                        if d3 == 10:
                            d3 = 0
        q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)
        e1 = 1 if d0 == 9 else 0
        e2 = 1 if (e1 and d1 == 9) else 0
        e3 = 1 if (e2 and d2 == 9) else 0
        ena = e1 | (e2 << 1) | (e3 << 2)
        out.append({'ena': ena, 'q': q})
        if 'mid' in row:
            for k, v in row['mid'].items():
                if k == 'reset':
                    cur_reset = v
    return out
