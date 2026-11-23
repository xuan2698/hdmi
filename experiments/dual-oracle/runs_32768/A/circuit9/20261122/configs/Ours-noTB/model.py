def reference(vectors):
    q = 0
    prev_a = 1
    out = []
    for v in vectors:
        a = v['a'] & 1
        if a:
            q = 4
        else:
            if prev_a == 0:
                q = (q + 1) % 7
        prev_a = a
        out.append({'q': q})
    return out
