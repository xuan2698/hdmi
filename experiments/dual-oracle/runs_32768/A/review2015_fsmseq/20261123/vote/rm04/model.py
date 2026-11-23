def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        reset = int(row.get('reset', 0))
        data = int(row.get('data', 0))
        if reset:
            state = 0
        else:
            if state == 0:
                if data:
                    state = 1
            elif state == 1:
                state = 2 if data else 0
            elif state == 2:
                state = 3 if data == 0 else 2
            elif state == 3:
                state = 4 if data else 0
        out.append({'start_shifting': 1 if state == 4 else 0})
    return out
