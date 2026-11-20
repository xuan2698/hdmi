def reference(vectors):
    out = []
    state = None
    for v in vectors:
        areset = v.get('areset')
        x = v.get('x')
        if areset == 1:
            state = 'S0'
            z = 0
        else:
            if state is None:
                state = 'S0'
            if state == 'S0':
                if x == 1:
                    state = 'S1'
                    z = 1
                else:
                    state = 'S0'
                    z = 0
            else:
                z = x
        out.append({'z': z})
    return out
