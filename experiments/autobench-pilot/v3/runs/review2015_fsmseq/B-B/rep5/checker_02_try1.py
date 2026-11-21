def reference(vectors):
    state = 0
    start = 0
    out = []
    for row in vectors:
        if row.get('reset', 0):
            state = 0
            start = 0
        else:
            d = row.get('data', 0)
            if start:
                pass
            elif state == 0:
                state = 1 if d == 1 else 0
            elif state == 1:
                state = 2 if d == 1 else 0
            elif state == 2:
                state = 2 if d == 1 else 3
            elif state == 3:
                if d == 1:
                    start = 1
                    state = 2
                else:
                    state = 0
        out.append({'start_shifting': start})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
                start = 0
            elif 'data' in m:
                d = m['data']
                if start:
                    pass
                elif state == 0:
                    state = 1 if d == 1 else 0
                elif state == 1:
                    state = 2 if d == 1 else 0
                elif state == 2:
                    state = 2 if d == 1 else 3
                elif state == 3:
                    if d == 1:
                        start = 1
                        state = 2
                    else:
                        state = 0
    return out
