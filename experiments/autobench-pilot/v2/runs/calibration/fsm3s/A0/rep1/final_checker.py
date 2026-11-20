def reference(vectors):
    state = None
    out = []
    for v in vectors:
        if v.get('reset'):
            state = 'A'
        else:
            if state is None:
                state = 'A'
            inp = v.get('in', 0)
            if state == 'A':
                state = 'B' if inp else 'A'
            elif state == 'B':
                state = 'B' if inp else 'C'
            elif state == 'C':
                state = 'D' if inp else 'A'
            elif state == 'D':
                state = 'B' if inp else 'C'
        o = 1 if state == 'D' else 0
        out.append({'out': o})
    return out
