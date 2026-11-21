def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)
        if areset:
            state = 0
        else:
            if state == 0:
                state = 0 if x == 0 else 1
            elif state == 1:
                state = 1 if x == 0 else 2
            else:
                state = 2
        z = 0 if state == 0 else 1
        mid = row.get('mid')
        if mid:
            if 'areset' in mid:
                areset = mid['areset']
            if 'x' in mid:
                x = mid['x']
            if areset:
                state = 0
            else:
                if state == 0:
                    state = 0 if x == 0 else 1
                elif state == 1:
                    state = 1 if x == 0 else 2
                else:
                    state = 2
        out.append({'z': z})
    return out
