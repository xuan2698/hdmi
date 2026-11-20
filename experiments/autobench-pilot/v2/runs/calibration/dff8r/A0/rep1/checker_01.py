def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        d = v['d'] & 0xFF
        reset = v['reset'] & 1
        if reset:
            q = 0
        else:
            q = d
        out.append({'q': q & 0xFF})
    return out
