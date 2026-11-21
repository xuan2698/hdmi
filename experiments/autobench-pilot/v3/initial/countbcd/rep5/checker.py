def reference(vectors):
    q = 0
    ena = 0
    out = []
    for row in vectors:
        if row.get('reset'):
            q = 0
            ena = 0
        else:
            d0 = q & 0xF
            d1 = (q >> 4) & 0xF
            d2 = (q >> 8) & 0xF
            d3 = (q >> 12) & 0xF
            e0 = 1
            e1 = 1 if d0 == 9 else 0
            e2 = 1 if (d0 == 9 and d1 == 9) else 0
            e3 = 1 if (d0 == 9 and d1 == 9 and d2 == 9) else 0
            ena = (e1 << 0) | (e2 << 1) | (e3 << 2)
            if e0:
                d0 += 1
                if d0 == 10:
                    d0 = 0
            if e1:
                d1 += 1
                if d1 == 10:
                    d1 = 0
            if e2:
                d2 += 1
                if d2 == 10:
                    d2 = 0
            if e3:
                d3 += 1
                if d3 == 10:
                    d3 = 0
            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)
        out.append({'q': q, 'ena': ena})
    return out
