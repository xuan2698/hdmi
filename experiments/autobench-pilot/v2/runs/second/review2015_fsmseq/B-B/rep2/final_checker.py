def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        reset = v.get('reset', 0)
        data = v.get('data', 0)
        if reset:
            state = 0
        else:
            if state == 0:
                state = 1 if data == 1 else 0
            elif state == 1:
                state = 2 if data == 1 else 1
            elif state == 2:
                state = 2 if data == 1 else 3
            elif state == 3:
                state = 4 if data == 1 else 0
            elif state == 4:
                state = 4
        out.append({'start_shifting': 1 if state == 4 else 0})
    return out
