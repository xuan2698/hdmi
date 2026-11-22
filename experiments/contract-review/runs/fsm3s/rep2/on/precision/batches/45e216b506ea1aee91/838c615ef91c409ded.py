def reference(vectors):
    state = 0
    res = []
    for v in vectors:
        r = v.get('reset', 0)
        i = v.get('in', 0)
        if r:
            state = 0
        else:
            if state == 0:
                state = 0 if i == 0 else 1
            elif state == 1:
                state = 2 if i == 0 else 1
            elif state == 2:
                state = 0 if i == 0 else 3
            else:
                state = 2 if i == 0 else 1
        res.append({'out': 1 if state == 3 else 0})
    return res