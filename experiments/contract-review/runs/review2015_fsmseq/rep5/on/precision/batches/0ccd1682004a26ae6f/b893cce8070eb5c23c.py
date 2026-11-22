def reference(vectors):
    state = 0
    start = 0
    out = []
    for v in vectors:
        reset = v.get('reset', 0)
        data = v.get('data', 0)
        if reset == 1:
            state = 0
            start = 0
        else:
            if state == 4:
                state = 4
                start = 1
            elif state == 3:
                if data == 1:
                    state = 4
                    start = 1
                else:
                    state = 0
                    start = 0
            elif state == 2:
                if data == 1:
                    state = 2
                else:
                    state = 3
                start = 0
            elif state == 1:
                if data == 1:
                    state = 2
                else:
                    state = 0
                start = 0
            else:
                if data == 1:
                    state = 1
                else:
                    state = 0
                start = 0
        out.append({'start_shifting': start})
    return out