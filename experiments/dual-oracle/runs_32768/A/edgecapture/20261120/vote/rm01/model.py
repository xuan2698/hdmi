def reference(vectors):
    o = 0
    p = 0
    M = 0xFFFFFFFF
    r = []
    for v in vectors:
        rst = v.get('reset', 0) & 1
        x = v.get('in', 0) & M
        if rst:
            o = 0
        else:
            o = (o | (p & (~x & M))) & M
        p = x
        r.append({'out': o})
    return r
