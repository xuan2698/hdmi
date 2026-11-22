def reference(vectors):
    state = 'S0'
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        x = v.get('x', 0)
        if areset == 1:
            state = 'S0'
            z = x if state == 'S0' else (1 - x)
            out.append({'z': z})
            continue
        if state == 'S0':
            z = x
        else:
            z = 1 - x
        out.append({'z': z})
        if state == 'S0':
            if x == 1:
                state = 'S1'
        else:
            state = 'S1'
    return out
