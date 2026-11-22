def reference(vectors):
    state = 0
    out = []
    for v in vectors:
        reset = v['reset']
        data = v['data']
        if reset == 1:
            state = 0
            out.append({'start_shifting': 0})
        else:
            if state == 4:
                out.append({'start_shifting': 1})
            else:
                if state == 3 and data == 1:
                    out.append({'start_shifting': 1})
                else:
                    out.append({'start_shifting': 0})
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 0
                elif state == 2:
                    state = 3 if data == 0 else 2
                elif state == 3:
                    state = 4 if data == 1 else 0
    return out
