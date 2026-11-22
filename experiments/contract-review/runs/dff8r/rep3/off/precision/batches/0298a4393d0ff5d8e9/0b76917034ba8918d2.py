def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        d = v['d'] & 0xFF
        r = v['reset'] & 1
        prev = q
        if r:
            q = 0
        else:
            q = d
        out.append({'q': prev})
    return out