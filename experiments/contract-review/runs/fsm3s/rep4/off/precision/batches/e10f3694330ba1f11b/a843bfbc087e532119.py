def reference(vectors):
    state = 'A'
    out = []
    for v in vectors:
        if v.get('reset', 0) == 1:
            state = 'A'
        else:
            i = v.get('in', 0)
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
