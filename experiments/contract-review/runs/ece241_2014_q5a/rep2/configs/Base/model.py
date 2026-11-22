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
                if x == 0:
                    state = 0
                else:
                    state = 1
            elif state == 1:
                if x == 0:
                    state = 1
                else:
                    state = 2
            else:
                state = 2
        z = 1 if state == 2 else (0 if state == 0 else 1)
        if state == 0:
            z = 0
        elif state == 1:
            z = 1
        else:
            z = 1
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
                    if x == 0:
                        state = 0
                    else:
                        state = 1
                elif state == 1:
                    if x == 0:
                        state = 1
                    else:
                        state = 2
                else:
                    state = 2
        out.append({'z': z})
    return out
