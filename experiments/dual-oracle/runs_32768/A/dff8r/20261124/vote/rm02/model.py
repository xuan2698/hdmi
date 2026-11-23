def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        if v['reset']:
            q = 0
        else:
            q = v['d'] & 0xFF
        out.append({'q': q})
    return out
