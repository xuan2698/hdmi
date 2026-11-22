def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        d = v['d']
        r = v['r']
        if r == 1:
            q = 0
        else:
            q = d
        out.append({'q': q})
    return out