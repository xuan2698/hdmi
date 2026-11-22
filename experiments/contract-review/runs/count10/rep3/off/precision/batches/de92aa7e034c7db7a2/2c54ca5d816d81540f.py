def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        if r == 1:
            q = 0
        else:
            if q == 9:
                q = 0
            else:
                q = q + 1
        out.append({'q': q})
    return out
