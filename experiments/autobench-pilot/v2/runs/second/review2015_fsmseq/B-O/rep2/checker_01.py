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
                if data == 1:
                    state = 1
                else:
                    state = 0
            elif state == 1:
                if data == 1:
                    state = 2
                else:
                    state = 0
            elif state == 2:
                if data == 0:
                    state = 3
                else:
                    state = 2
            elif state == 3:
                if data == 1:
                    state = 4
                else:
                    state = 0
            if state == 4:
                start = 1
            else:
                start = 0
        out.append({'start_shifting': start})
    return out
