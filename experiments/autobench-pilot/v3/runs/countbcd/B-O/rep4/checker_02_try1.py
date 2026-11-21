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
            e1 = 1 if d0 == 9 else 0
            e2 = 1 if (d0 == 9 and d1 == 9) else 0
            e3 = 1 if (d0 == 9 and d1 == 9 and d2 == 9) else 0
            ena = (e3 << 2) | (e2 << 1) | e1
            d0 = (d0 + 1) % 10
            if e1:
                d1 = (d1 + 1) % 10
            if e2:
                d2 = (d2 + 1) % 10
            if e3:
                d3 = (d3 + 1) % 10
            q = d0 | (d1 << 4) | (d2 << 8) | (d3 << 12)
        out.append({'q': q, 'ena': ena})
    return out
