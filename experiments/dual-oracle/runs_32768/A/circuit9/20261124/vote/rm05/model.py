def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        a = v['a'] if isinstance(v, dict) else v
        if a:
            q = 4
        else:
            q = 0 if q == 6 else q + 1
        out.append({'q': q})
    return out
