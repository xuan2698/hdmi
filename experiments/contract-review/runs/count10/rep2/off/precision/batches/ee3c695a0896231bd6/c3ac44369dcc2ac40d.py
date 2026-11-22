def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        if v['reset'] == 1:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
    return out