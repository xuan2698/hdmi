def reference(vectors):
    IDLE, S1, S11, S110, FOUND = 0, 1, 2, 3, 4
    state = IDLE
    out = []
    for row in vectors:
        if isinstance(row, dict):
            r = row['reset']
            d = row['data']
        else:
            r = row[0]
            d = row[1]
        if r:
            state = IDLE
        else:
            if state == IDLE:
                state = S1 if d else IDLE
            elif state == S1:
                state = S11 if d else IDLE
            elif state == S11:
                state = S11 if d else S110
            elif state == S110:
                state = FOUND if d else IDLE
            else:
                state = FOUND
        out.append({'start_shifting': 1 if state == FOUND else 0})
    return out
