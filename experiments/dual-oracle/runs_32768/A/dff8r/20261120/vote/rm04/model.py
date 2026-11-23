def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        r = v.get('reset', 0)
        d = v.get('d', 0)
        q = 0 if r else (d & 255)
        out.append({'q': q})
    return out
