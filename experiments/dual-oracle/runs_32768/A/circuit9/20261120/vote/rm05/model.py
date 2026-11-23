def reference(vectors):
    q = 0
    pa = 0
    pc = 0
    res = []
    for v in vectors:
        a = v.get('a', 0)
        c = v.get('clk', None)
        if c is None:
            pos = True
        else:
            pos = (c == 1 and pc == 0)
            pc = c
        if pos:
            if a == 1:
                q = 4
            elif pa == 0:
                q = (q + 1) % 7
            pa = a
        res.append({'q': q})
    return res
