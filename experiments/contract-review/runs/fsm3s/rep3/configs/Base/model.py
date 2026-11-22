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
                state = 1 if inp else 0
            elif state == 1:
                state = 2 if not inp else 1
            elif state == 2:
                state = 3 if inp else 0
            elif state == 3:
                state = 2 if not inp else 1
        o = 1 if state == 3 else 0
        out.append({'out': o})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
            else:
                mi = m.get('in', inp)
                if state == 0:
                    state = 1 if mi else 0
                elif state == 1:
                    state = 2 if not mi else 1
                elif state == 2:
                    state = 3 if mi else 0
                elif state == 3:
                    state = 2 if not mi else 1
    return out
