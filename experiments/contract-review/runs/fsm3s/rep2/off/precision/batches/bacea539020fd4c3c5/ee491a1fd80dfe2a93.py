def reference(vectors):
    state = 'A'
    out = []
    for v in vectors:
        if v['reset'] == 1:
            state = 'A'
        else:
            if state == 'A':
                state = 'B' if v['in'] == 1 else 'A'
            elif state == 'B':
                state = 'B' if v['in'] == 1 else 'C'
            elif state == 'C':
                state = 'D' if v['in'] == 1 else 'A'
            elif state == 'D':
                state = 'B' if v['in'] == 1 else 'C'
        out.append({'out': 1 if state == 'D' else 0})
    return out
