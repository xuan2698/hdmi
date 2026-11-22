def reference(vectors):
    state = 'S0'
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        x = v.get('x', 0)
        if areset:
            state = 'S0'
            z = 0
        else:
            if state == 'S0':
                z = x
            else:
                z = 1 - x
        out.append({'z': z})
        if not areset:
            if state == 'S0' and x == 1:
                state = 'S1'
    return out
