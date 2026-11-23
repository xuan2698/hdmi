def reference(vectors):
    st = 0
    out = []
    pc = 0
    pa = 0
    pb = 0
    has_clk = bool(vectors) and ('clk' in vectors[0])
    for r in vectors:
        a = int(r.get('a', 0)) & 1
        b = int(r.get('b', 0)) & 1
        if has_clk:
            c = int(r.get('clk', 0)) & 1
            if c == 1 and pc == 0:
                st = 1 if (pa + pb + st) >= 2 else 0
            pc = c
            pa = a
            pb = b
        else:
            st = 1 if (a + b + st) >= 2 else 0
        q = (a ^ b ^ st) & 1
        out.append({'q': q, 'state': st})
    return out
