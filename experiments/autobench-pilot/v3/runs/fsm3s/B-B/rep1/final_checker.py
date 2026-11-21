def reference(vectors):
    state = 0
    out = []
    trans = {
        0: {0: 0, 1: 1},
        1: {0: 2, 1: 1},
        2: {0: 0, 1: 3},
        3: {0: 2, 1: 1},
    }
    for row in vectors:
        inp = row.get('in', 0)
        rst = row.get('reset', 0)
        if rst:
            state = 0
        else:
            state = trans[state][inp]
        o = 1 if state == 3 else 0
        out.append({'out': o})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
            elif 'in' in m:
                state = trans[state][m['in']]
    return out
