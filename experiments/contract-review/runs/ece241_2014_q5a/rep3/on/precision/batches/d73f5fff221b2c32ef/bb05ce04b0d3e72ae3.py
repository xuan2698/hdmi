def reference(vectors):
    state = 'A'
    outputs = []
    for v in vectors:
        areset = v.get('areset', 0)
        x = v.get('x', 0)
        if areset:
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
        z = 1 if state == 'B' else 0
        outputs.append({'z': z})
    return outputs