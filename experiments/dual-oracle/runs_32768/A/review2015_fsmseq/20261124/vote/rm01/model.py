def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        reset = row['reset']
        data = row['data']
        if reset:
            state = 0
        elif state != 4:
            if state == 0:
                state = 1 if data else 0
            elif state == 1:
                state = 2 if data else 0
            elif state == 2:
                state = 3 if data == 0 else 2
            elif state == 3:
                state = 4 if data else 0
        out.append({'start_shifting': 1 if state == 4 else 0})
    return out
