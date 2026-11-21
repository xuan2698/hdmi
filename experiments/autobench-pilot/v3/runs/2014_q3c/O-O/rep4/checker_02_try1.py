def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        x = row.get('x', 0)
        y = row.get('y', state)
        state = y
        if state == 0:
            nxt = 1 if x else 0
            z = 0
        elif state == 1:
            nxt = 4 if x else 1
            z = 0
        elif state == 2:
            nxt = 1 if x else 2
            z = 0
        elif state == 3:
            nxt = 2 if x else 1
            z = 1
        elif state == 4:
            nxt = 4 if x else 3
            z = 1
        else:
            nxt = 0
            z = 0
        state = nxt
        out.append({'Y0': state & 1, 'z': z})
        if 'mid' in row:
            m = row['mid']
            if 'x' in m:
                x = m['x']
            if 'y' in m:
                state = m['y']
            if state == 0:
                nxt = 1 if x else 0
                z = 0
            elif state == 1:
                nxt = 4 if x else 1
                z = 0
            elif state == 2:
                nxt = 1 if x else 2
                z = 0
            elif state == 3:
                nxt = 2 if x else 1
                z = 1
            elif state == 4:
                nxt = 4 if x else 3
                z = 1
            else:
                nxt = 0
                z = 0
            state = nxt
    return out
