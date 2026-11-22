def reference(vectors):
    state = 0
    start_shifting = 0
    inputs = {'reset': 0, 'data': 0}
    outputs = []
    for vec in vectors:
        if 'reset' in vec:
            inputs['reset'] = vec['reset']
        if 'data' in vec:
            inputs['data'] = vec['data']
        reset = inputs['reset']
        data = inputs['data']
        if reset == 1:
            next_state = 0
            next_start = 0
        else:
            if state == 4:
                next_state = 4
                next_start = 1
            elif state == 3 and data == 1:
                next_state = 4
                next_start = 1
            else:
                next_start = 0
                if state == 0:
                    if data == 0:
                        next_state = 0
                    else:
                        next_state = 1
                elif state == 1:
                    if data == 0:
                        next_state = 0
                    else:
                        next_state = 2
                elif state == 2:
                    if data == 0:
                        next_state = 3
                    else:
                        next_state = 2
                elif state == 3:
                    next_state = 0
                else:
                    next_state = 0
        state = next_state
        start_shifting = next_start
        outputs.append({'start_shifting': start_shifting})
        mid = vec.get('mid')
        if mid:
            for k, v in mid.items():
                inputs[k] = v
    return outputs