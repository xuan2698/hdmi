def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        if row.get('areset', 0):
            state = 0
        else:
            x = row.get('x', 0)
            if state == 0:
                z = x
                if x == 1:
                    state = 1
            else:
                z = 1 - x
        out.append({'z': z})
        if 'mid' in row:
            m = row['mid']
            if m.get('areset', 0):
                state = 0
            elif 'x' in m:
                x = m['x']
                if state == 0:
                    if x == 1:
                        state = 1
                else:
                    pass
    return out
