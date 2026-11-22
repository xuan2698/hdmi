def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        if r == 1:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
    return out
