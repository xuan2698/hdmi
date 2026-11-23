def reference(vectors):
    q = 0
    pc = 0
    out = []
    for v in vectors:
        c = v.get('clk', 0)
        a = v.get('a', 0)
        if c == 1 and pc == 0:
            if a:
                q = 4
            else:
                q = 0 if q == 6 else (q + 1) & 7
        out.append({'q': q})
        pc = c
    return out
