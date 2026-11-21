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
            if d[0] == 9:
                e[0] = 1
                if d[1] == 9:
                    e[1] = 1
                    if d[2] == 9:
                        e[2] = 1
            ena = e[0] | (e[1] << 1) | (e[2] << 2)
            d[0] = (d[0] + 1) % 10
            for i in range(3):
                if e[i]:
                    d[i + 1] = (d[i + 1] + 1) % 10
            q = sum(d[i] << (4 * i) for i in range(4))
        out.append({'q': q, 'ena': ena})
    return out
