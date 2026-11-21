def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        data = row.get('data', 0)
        if reset:
            state = 0
        else:
            if state == 0:
                state = 1 if data == 1 else 0
            elif state == 1:
                state = 2 if data == 1 else 0
            elif state == 2:
                state = 2 if data == 1 else 3
            elif state == 3:
                state = 4 if data == 1 else 0
            elif state == 4:
                state = 4
        out.append({'start_shifting': 1 if state == 4 else 0})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
            elif 'data' in m:
                data = m['data']
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 0
                elif state == 2:
                    state = 2 if data == 1 else 3
                elif state == 3:
                    state = 4 if data == 1 else 0
                elif state == 4:
                    state = 4
    return out
