def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        reset = v['reset']
        data = v['data']
        if reset:
            state = 0
            start = 0
        else:
            if state == 0:
                state = 1 if data == 1 else 0
            elif state == 1:
                state = 2 if data == 1 else 0
            elif state == 2:
                state = 2 if data == 1 else 3
            elif state == 3:
                state = 4 if data == 1 else 0
            elif state == 4:
                state = 4
            start = 1 if state == 4 else 0
        out.append({'start_shifting': start})
    return out
