def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        reset = v['reset'] if isinstance(v, dict) else v[0]
        if reset:
            q = 0
        else:
            q = (q + 1) % 10
        out.append({'q': q})
    return out
