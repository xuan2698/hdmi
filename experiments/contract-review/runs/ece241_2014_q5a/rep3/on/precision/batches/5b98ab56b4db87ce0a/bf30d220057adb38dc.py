def reference(vectors):
    state = 'A'
    out = []
    for v in vectors:
        areset = v.get('areset', 0)
        x = v.get('x', 0)
        if areset == 1:
            state = 'A'
        else:
            if state == 'A':
                if x == 1:
                    state = 'B'
                else:
                    state = 'A'
            elif state == 'B':
                if x == 1:
                    state = 'C'
                else:
                    state = 'B'
            else:
                if x == 1:
                    state = 'C'
                else:
                    state = 'B'
        if state == 'B':
            z = 1
        else:
            z = 0
        out.append({'z': z})
    return out
