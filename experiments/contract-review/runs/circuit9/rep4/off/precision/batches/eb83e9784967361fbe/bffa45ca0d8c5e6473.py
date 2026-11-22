def reference(vectors):
    q = 4
    prev_a = 1
    out = []
    for v in vectors:
        a = v['a']
        if prev_a == 0:
            q = (q + 1) & 7
        out.append({'q': q})
        prev_a = a
    return out