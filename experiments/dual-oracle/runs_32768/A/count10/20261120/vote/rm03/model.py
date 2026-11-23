def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        if r:
            q = 0
        elif q == 9:
            q = 0
        else:
            q += 1
        out.append({'q': q})
    return out
