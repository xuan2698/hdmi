def reference(vectors):
    q = 4
    out = []
    for v in vectors:
        a = v['a']
        if a:
            q = 4
        else:
            q = (q + 1) % 7
        out.append({'q': q})
    return out
