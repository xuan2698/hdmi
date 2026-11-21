def reference(vectors):
    q = 0
    ena = 0
    out = []
    for row in vectors:
        if row.get('reset'):
            q = 0
            ena = 0
        else:
            d = [(q >> (4 * i)) & 0xF for i in range(4)]
            e = [0, 0, 0]
            e[0] = 1 if d[0] == 9 else 0
            e[1] = 1 if (d[1] == 9 and e[0]) else 0
            e[2] = 1 if (d[2] == 9 and e[1]) else 0
            ena = (e[2] << 2) | (e[1] << 1) | e[0]
            if e[0]:
                d[0] = 0
                d[1] = (d[1] + 1) % 10
            if e[1]:
                d[1] = 0
                d[2] = (d[2] + 1) % 10
            if e[2]:
                d[2] = 0
                d[3] = (d[3] + 1) % 10
            q = sum(d[i] << (4 * i) for i in range(4))
        out.append({'q': q, 'ena': ena})
    return out
