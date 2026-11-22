def reference(vectors):
    q = None
    prev_a = None
    out = []
    for v in vectors:
        a = v['a']
        if q is None:
            q = 4
        elif a == 0 and prev_a == 0:
            q = (q + 1) % 8
        out.append({'q': q})
        prev_a = a
    return out