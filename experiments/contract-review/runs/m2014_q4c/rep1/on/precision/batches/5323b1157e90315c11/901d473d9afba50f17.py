def reference(vectors):
    q = 0
    out = []
    for vec in vectors:
        d = vec.get('d', 0)
        r = vec.get('r', 0)
        if r == 1:
            q = 0
        else:
            q = d
        out.append({'q': q})
    return out
