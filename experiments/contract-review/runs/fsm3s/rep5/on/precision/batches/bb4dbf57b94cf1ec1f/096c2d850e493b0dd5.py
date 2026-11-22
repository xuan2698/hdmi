def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        if v['reset']:
            state = 0
        else:
            i = v['in']
            if state == 0:
                state = 0 if i == 0 else 1
            elif state == 1:
                state = 2 if i == 0 else 1
            elif state == 2:
                state = 0 if i == 0 else 3
            else:
                state = 2 if i == 0 else 1
        out.append({'out': 1 if state == 3 else 0})
    return out