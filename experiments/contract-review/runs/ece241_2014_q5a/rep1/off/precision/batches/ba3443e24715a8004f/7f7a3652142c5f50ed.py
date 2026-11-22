def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        a = v.get('areset', 0)
        x = v.get('x', 0)
        if a:
            state = 0
            out.append({'z': 0})
        else:
            if state == 0:
                z = x
                if x == 1:
                    state = 1
            else:
                z = 1 - x
            out.append({'z': z})
    return out