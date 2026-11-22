def reference(vectors):
    q = 0x34
    out = []
    for v in vectors:
        d = v['d'] & 0xFF
        r = v['reset'] & 1
        if r:
            q = 0x34
        else:
            q = d
        out.append({'q': q})
    return out
