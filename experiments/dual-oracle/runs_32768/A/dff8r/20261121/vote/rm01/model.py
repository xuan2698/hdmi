def reference(vectors):
    q = 0
    pc = 0
    out = []
    for r in vectors:
        c = r.get('clk', 0)
        if c == 1 and pc == 0:
            if r.get('reset', 0):
                q = 0
            else:
                q = r.get('d', 0) & 0xff
        pc = c
        out.append({'q': q & 0xff})
    return out
