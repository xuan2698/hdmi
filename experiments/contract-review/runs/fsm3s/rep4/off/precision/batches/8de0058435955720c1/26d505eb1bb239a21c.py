def reference(vectors):
    state = 'A'
    outs = []
    for v in vectors:
        if v.get('reset', 0) == 1:
            state = 'A'
        else:
            i = v.get('in', 0)
            if state == 'A':
                state = 'B' if i == 1 else 'A'
            elif state == 'B':
                state = 'B' if i == 1 else 'C'
            elif state == 'C':
                state = 'D' if i == 1 else 'A'
            elif state == 'D':
                state = 'B' if i == 1 else 'C'
        outs.append({'out': 1 if state == 'D' else 0})
    return outs
