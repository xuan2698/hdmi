def reference(vectors):
    state = 'A'
    out = []
    for v in vectors:
        i = v['in']; r = v['reset']
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
        out.append({'out': 1 if state == 'D' else 0})
    return out
