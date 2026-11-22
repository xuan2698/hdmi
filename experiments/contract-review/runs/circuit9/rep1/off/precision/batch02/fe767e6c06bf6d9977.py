def reference(vectors):
    q = None
    out = []
    for v in vectors:
        a = v['a']
        if q is None:
            q = 4
        elif a == 0:
            q = (q + 1) % 8
        out.append({'q': q})
    return out