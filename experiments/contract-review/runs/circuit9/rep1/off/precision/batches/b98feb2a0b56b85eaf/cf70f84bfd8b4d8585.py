def reference(vectors):
    q = None
    out = []
    for v in vectors:
        a = v['a']
        if q is None:
            q = 4
        else:
            if a == 1:
                pass
            else:
                q = (q + 1) % 8
        out.append({'q': q})
    return out