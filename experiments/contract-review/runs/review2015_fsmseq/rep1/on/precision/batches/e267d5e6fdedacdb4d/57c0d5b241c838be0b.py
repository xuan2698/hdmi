def reference(vectors):
    state = 0
    res = []
    for row in vectors:
        reset = row['reset']
        data = row['data']
        if reset == 1:
            out = 0
        elif state == 4:
            out = 1
        elif state == 3 and data == 1:
            out = 1
        else:
            out = 0
        res.append({'start_shifting': out})
        if reset == 1:
            state = 0
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
            if data == 1:
                state = 4
            else:
                state = 0
        else:
            state = 4
    return res