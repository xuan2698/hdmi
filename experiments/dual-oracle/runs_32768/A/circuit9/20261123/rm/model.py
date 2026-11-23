def reference(vectors):
    c = 4
    out = []
    for v in vectors:
        a = v['a']
        q = c
        if a:
            c = 4
        else:
            c = 0 if c == 6 else c + 1
        out.append({'q': q})
    return out
