def reference(vectors):
    state = 0
    z = 0
    out = []
    for row in vectors:
        if row.get('areset'):
            state = 0
            z = 0
        else:
            x = row.get('x', 0)
            if state == 0:
                if x == 0:
                    z = 0
                    state = 0
                else:
                    z = 1
                    state = 1
            else:
                z = 1 - x
                state = 1
        out.append({'z': z})
        if 'mid' in row:
            m = row['mid']
            if m.get('areset'):
                state = 0
                z = 0
            elif 'x' in m:
                x = m['x']
                if state == 0:
                    if x == 0:
                        z = 0
                        state = 0
                    else:
                        z = 1
                        state = 1
                else:
                    z = 1 - x
                    state = 1
    return out
