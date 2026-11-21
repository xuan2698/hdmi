def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        inp = row.get('in', 0)
        rst = row.get('reset', 0)
        if rst:
            state = 0
        else:
            if state == 0:
                state = 0 if inp == 0 else 1
            elif state == 1:
                state = 2 if inp == 0 else 1
            elif state == 2:
                state = 0 if inp == 0 else 3
            elif state == 3:
                state = 2 if inp == 0 else 1
        o = 1 if state == 3 else 0
        out.append({'out': o})
        if 'mid' in row:
            m = row['mid']
            if 'reset' in m and m['reset']:
                state = 0
            elif 'in' in m:
                inp = m['in']
                if state == 0:
                    state = 0 if inp == 0 else 1
                elif state == 1:
                    state = 2 if inp == 0 else 1
                elif state == 2:
                    state = 0 if inp == 0 else 3
                elif state == 3:
                    state = 2 if inp == 0 else 1
    return out
