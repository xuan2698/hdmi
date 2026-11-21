def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        x = row.get('x', 0)
        if 'y' in row:
            state = row['y']
        def step(s, x):
            if s == 0:
                return (1 if x else 0, 0)
            if s == 1:
                return (4 if x else 1, 0)
            if s == 2:
                return (1 if x else 2, 0)
            if s == 3:
                return (2 if x else 1, 1)
            if s == 4:
                return (4 if x else 3, 1)
            return (0, 0)
        nxt, z = step(state, x)
        out.append({'Y0': nxt & 1, 'z': z})
        state = nxt
        if 'mid' in row:
            m = row['mid']
            if 'y' in m:
                state = m['y']
            if 'x' in m:
                x = m['x']
            nxt, z = step(state, x)
            state = nxt
    return out
