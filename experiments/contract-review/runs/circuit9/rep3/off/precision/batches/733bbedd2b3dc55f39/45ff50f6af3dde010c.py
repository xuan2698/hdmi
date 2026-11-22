def reference(vectors):
    q = 4
    prev_a = None
    out = []
    for v in vectors:
        a = v['a']
        if a == 1:
            pass
        else:
            if prev_a == 1:
                pass
            else:
                q = (q + 1) % 8
        out.append({'q': q})
        prev_a = a
    return out