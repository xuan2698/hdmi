def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        if v.get('reset', 0):
            q = 0
        else:
            q = v.get('d', 0) & 0xFF
        out.append({'q': q})
    return out
