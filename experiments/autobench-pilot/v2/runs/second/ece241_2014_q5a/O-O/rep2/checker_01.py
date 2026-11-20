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
                if x == 0:
                    z = 0
                    state = 'S0'
                else:
                    z = 1
                    state = 'S1'
            else:
                if x == 0:
                    z = 1
                    state = 'S1'
                else:
                    z = 0
                    state = 'S1'
        out.append({'z': z})
    return out
