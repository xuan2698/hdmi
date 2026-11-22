def reference(vectors):
    q = 4
    prev_a = 1
    out = []
    for v in vectors:
        a = v['a']
        if a == 0 and prev_a == 1:
            q = (q + 1) % 8
        out.append({'q': q})
        prev_a = a
    return out