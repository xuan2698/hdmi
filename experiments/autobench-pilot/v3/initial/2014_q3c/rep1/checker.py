def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        x = row.get('x', 0)
        y = row.get('y', 0)
        if 'y' in row:
            state = y & 7
        nxt = {
            (0,0):0,(0,1):1,
            (1,0):1,(1,1):4,
            (2,0):2,(2,1):1,
            (3,0):1,(3,1):2,
            (4,0):3,(4,1):4,
        }
        zmap = {0:0,1:0,2:0,3:1,4:1}
        Y = nxt.get((state,x), state)
        z = zmap.get(state, 0)
        out.append({'Y0': Y & 1, 'z': z & 1})
        state = Y
        if 'mid' in row:
            m = row['mid']
            if 'x' in m:
                x = m['x']
            if 'y' in m:
                state = m['y'] & 7
    return out
