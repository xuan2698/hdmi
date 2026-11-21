def reference(vectors):
    q = 0
    ena = 0
    out = []
    for row in vectors:
        if row.get('reset'):
            q = 0
            ena = 0
        else:
            d = [(q >> (4*i)) & 0xF for i in range(4)]
            e = [1]
            for i in range(1, 4):
                e.append(1 if all(d[j] == 9 for j in range(i)) else 0)
            ena = sum(e[i] << (i-1) for i in range(1, 4))
            for i in range(4):
                if e[i]:
                    d[i] = (d[i] + 1) % 10
            q = sum(d[i] << (4*i) for i in range(4))
        out.append({'q': q, 'ena': ena})
    return out
