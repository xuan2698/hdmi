def reference(vectors):
    q = 52
    out = []
    for v in vectors:
        if v['reset'] == 1:
            q = 52
        else:
            q = v['d'] & 0xFF
        out.append({'q': q})
    return out