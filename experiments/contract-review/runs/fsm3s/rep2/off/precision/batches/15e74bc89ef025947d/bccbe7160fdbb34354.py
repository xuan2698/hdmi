def reference(vectors):
    state = 'A'
    out = []
    for v in vectors:
        i = v['in']
        r = v['reset']
        o = 1 if state == 'D' else 0
        out.append({'out': o})
        if r == 1:
            state = 'A'
        else:
            if state == 'A':
                state = 'B' if i == 1 else 'A'
            elif state == 'B':
                state = 'B' if i == 1 else 'C'
            elif state == 'C':
                state = 'D' if i == 1 else 'A'
            elif state == 'D':
                state = 'B' if i == 1 else 'C'
    return out
