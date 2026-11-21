def reference(vectors):
    state = 0
    found = 0
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        data = row.get('data', 0)
        if reset:
            state = 0
            found = 0
        else:
            if not found:
                if state == 0:
                    state = 1 if data else 0
                elif state == 1:
                    state = 2 if data else 1
                elif state == 2:
                    state = 2 if data else 3
                elif state == 3:
                    if data:
                        found = 1
                    else:
                        state = 0
        out.append({'start_shifting': found})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
                found = 0
            elif 'data' in m and not found:
                data = m['data']
                if state == 0:
                    state = 1 if data else 0
                elif state == 1:
                    state = 2 if data else 1
                elif state == 2:
                    state = 2 if data else 3
                elif state == 3:
                    if data:
                        found = 1
                    else:
                        state = 0
    return out
