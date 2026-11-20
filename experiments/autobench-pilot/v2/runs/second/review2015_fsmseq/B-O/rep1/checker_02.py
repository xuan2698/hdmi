def reference(vectors):
    out = []
    state = 0
    started = 0
    for v in vectors:
        reset = v.get('reset', 0)
        data = v.get('data', 0)
        if reset:
            state = 0
            started = 0
        else:
            if started:
                state = 4
            else:
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 0
                elif state == 2:
                    state = 2 if data == 1 else 3
                elif state == 3:
                    if data == 1:
                        state = 4
                        started = 1
                    else:
                        state = 0
        out.append({'start_shifting': started})
    return out
