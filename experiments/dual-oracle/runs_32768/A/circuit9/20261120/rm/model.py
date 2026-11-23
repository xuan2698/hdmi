def reference(vectors):
    q = 0
    r = []
    for v in vectors:
        if v['a']:
            q = 4
        else:
            q = 0 if q == 6 else q + 1
        r.append({'q': q})
    return r
