def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        x = v.get('x', 0)
        if areset:
            state = 0
            out.append({'z': 0})
        else:
            if state == 0:
                z = x
            else:
                z = 1 - x
            out.append({'z': z})
            if state == 0 and x == 1:
                state = 1
    return out
