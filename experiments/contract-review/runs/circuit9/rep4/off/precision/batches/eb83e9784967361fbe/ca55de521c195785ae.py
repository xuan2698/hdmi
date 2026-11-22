def reference(vectors):
    q = 4
    out = []
    for v in vectors:
        a = v['a']
        if a == 0:
            q = (q + 1) & 7
        out.append({'q': q})
    return out