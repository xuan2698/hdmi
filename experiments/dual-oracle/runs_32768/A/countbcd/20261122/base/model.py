def reference(vectors):
    q = 0
    cur = {'reset': 0}
    out = []
    for row in vectors:
        for k, v in row.items():
            if k != 'mid':
                cur[k] = v
        r = cur.get('reset', 0)
        if r:
            q = 0
        else:
            d0 = q & 15
            d1 = (q >> 4) & 15
            d2 = (q >> 8) & 15
            d3 = (q >> 12) & 15
            if d0 == 9:
                d0 = 0
                c1 = 1
            else:
                d0 += 1
                c1 = 0
            if c1:
                if d1 == 9:
                    d1 = 0
                    c2 = 1
                else:
                    d1 += 1
                    c2 = 0
            else:
                c2 = 0
            if c2:
                if d2 == 9:
                    d2 = 0
                    c3 = 1
                else:
                    d2 += 1
                    c3 = 0
            else:
                c3 = 0
            if c3:
                if d3 == 9:
                    d3 = 0
                else:
                    d3 += 1
            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)
        e1 = 1 if (q & 15) == 9 else 0
        e2 = 1 if (q & 255) == 0x99 else 0
        e3 = 1 if (q & 4095) == 0x999 else 0
        out.append({'ena': e1 | (e2 << 1) | (e3 << 2), 'q': q & 0xFFFF})
        if 'mid' in row:
            for k, v in row['mid'].items():
                cur[k] = v
    return out
