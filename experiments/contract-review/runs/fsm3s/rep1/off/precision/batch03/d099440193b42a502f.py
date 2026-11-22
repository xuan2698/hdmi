def reference(vectors):
    state = 'A'
    outs = []
    for v in vectors:
        r = v['reset']
        i = v['in']
        if r == 1:
            state = 'A'
        else:
            if state == 'A':
                state = 'A' if i == 0 else 'B'
            elif state == 'B':
                state = 'C' if i == 0 else 'B'
            elif state == 'C':
                state = 'A' if i == 0 else 'D'
            elif state == 'D':
                state = 'C' if i == 0 else 'B'
        outs.append({'out': 1 if state == 'D' else 0})
    return outs
