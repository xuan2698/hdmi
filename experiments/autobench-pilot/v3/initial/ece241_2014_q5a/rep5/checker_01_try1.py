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
                state = 1 if x else 0
            else:
                z = x ^ 1
                state = 1
        out.append({'z': z})
        if 'mid' in row:
            m = row['mid']
            if m.get('areset', 0):
                state = 0
            elif 'x' in m:
                x = m['x']
                if state == 0:
                    state = 1 if x else 0
                else:
                    state = 1
    return out
