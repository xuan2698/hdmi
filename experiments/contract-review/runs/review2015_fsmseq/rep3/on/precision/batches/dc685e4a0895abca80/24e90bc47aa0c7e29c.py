def reference(vectors):
    state = 0
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    outputs = []
    for vec in vectors:
        if 'reset' in vec:
            cur_reset = vec['reset']
        if 'data' in vec:
            cur_data = vec['data']
        reset = cur_reset
        data = cur_data
        if reset == 1:
            state = 0
            start_shifting = 0
        else:
            if state == 4:
                state = 4
            elif state == 3 and data == 1:
                state = 4
            elif state == 0:
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
                state = 0
            start_shifting = 1 if state == 4 else 0
        outputs.append({'start_shifting': start_shifting})
        if 'mid' in vec:
            mid = vec['mid']
            if mid:
                if 'reset' in mid:
                    cur_reset = mid['reset']
                if 'data' in mid:
                    cur_data = mid['data']
    return outputs