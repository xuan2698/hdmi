def reference(vectors):
    Q = 0
    out = []
    for v in vectors:
        d = v['d']
        r = v['r']
        if r == 1:
            Q = 0
        else:
            Q = d
        out.append({'q': Q})
    return out
