def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        if r == 1:
            q = 0
        else:
            q = 0 if q == 9 else q + 1
        out.append({'q': q})
    return out
