def reference(vectors):
    q = 4
    prev_a = None
    out = []
    for v in vectors:
        a = v['a']
        if prev_a is not None:
            if prev_a == 0:
                q = (q + 1) % 8
        out.append({'q': q})
        prev_a = a
    return out