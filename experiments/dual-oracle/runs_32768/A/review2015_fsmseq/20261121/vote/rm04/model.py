def reference(vectors):
    state = 0
    out = 0
    result = []
    for row in vectors:
        reset = row['reset']
        data = row['data']
        if reset:
            state = 0
            out = 0
        elif out == 0:
            if state == 0:
                if data == 1:
                    state = 1
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
                    out = 1
                else:
                    state = 0
        result.append({'start_shifting': out})
    return result
