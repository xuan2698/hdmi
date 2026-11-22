def reference(vectors):
    q = 0
    prev_a = 1
    out = []
    for v in vectors:
        a = v['a']
        if a == 0 and prev_a == 1:
            q = (q + 1) & 7
        out.append({'q': q})
        prev_a = a
    return out
