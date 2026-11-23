def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        a = v['a']
        if a:
            q = 4
        elif q == 6:
            q = 0
        else:
            q += 1
        out.append({'q': q})
    return out
