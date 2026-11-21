def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        x = row.get('x', 0)
        y = row.get('y', 0)
        state = y
        def logic(s, xv):
            if s == 0:
                return (1 if xv else 0), 0
            elif s == 1:
                return (4 if xv else 1), 0
            elif s == 2:
                return (1 if xv else 2), 0
            elif s == 3:
                return (2 if xv else 1), 1
            elif s == 4:
                return (4 if xv else 3), 1
            else:
                return 0, 0
        nxt, z = logic(state, x)
        res = {'Y0': nxt & 1, 'z': z}
        if 'mid' in row:
            m = row['mid']
            if 'x' in m:
                x = m['x']
            if 'y' in m:
                state = m['y']
            nxt, z = logic(state, x)
            res = {'Y0': nxt & 1, 'z': z}
        out.append(res)
    return out
