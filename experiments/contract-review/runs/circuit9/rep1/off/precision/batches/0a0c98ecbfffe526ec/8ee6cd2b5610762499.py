def reference(vectors):
    q = None
    prev_a = None
    out = []
    for v in vectors:
        a = v['a']
        if q is None:
            q = 4
        else:
            if a == 1:
                pass
            else:
                if not (q == 4 and prev_a == 1):
                    q = (q + 1) % 8
        out.append({'q': q})
        prev_a = a
    return out
