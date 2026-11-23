def reference(vectors):
    s = 4
    out = []
    for v in vectors:
        a = v['a']
        out.append({'q': s})
        if a:
            s = 4
        else:
            s = 0 if s == 6 else s + 1
    return out
