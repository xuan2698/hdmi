def reference(vectors):
    state = 0
    outputs = []
    for v in vectors:
        reset = v.get('reset', 0)
        data = v.get('data', 0)
        if reset:
            state = 0
            start = 0
        else:
            if state == 0:
                if data:
                    state = 1
                else:
                    state = 0
            elif state == 1:
                if data:
                    state = 2
                else:
                    state = 0
            elif state == 2:
                if data:
                    state = 2
                else:
                    state = 3
            elif state == 3:
                if data:
                    state = 4
                else:
                    state = 0
            else:
                state = 4
            start = 1 if state == 4 else 0
        outputs.append({'start_shifting': start})
    return outputs