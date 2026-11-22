def reference(vectors):
    state = 'A'
    z = 0
    persistent = {'areset': 0, 'x': 0}
    out = []
    for row in vectors:
        for k in row:
            if k != 'mid':
                persistent[k] = row[k]
        areset = persistent.get('areset', 0)
        x = persistent.get('x', 0)
        if areset == 1:
            state = 'A'
            z = 0
        else:
            if state == 'A':
                if x == 0:
                    state = 'A'
                    z = 0
                else:
                    state = 'C'
                    z = 1
            elif state == 'B':
                if x == 0:
                    state = 'C'
                    z = 1
                else:
                    state = 'B'
                    z = 0
            else:
                if x == 0:
                    state = 'C'
                    z = 1
                else:
                    state = 'B'
                    z = 0
        out.append({'z': z})
        mid = row.get('mid', {})
        if mid:
            for k, v in mid.items():
                persistent[k] = v
            if persistent.get('areset', 0) == 1:
                state = 'A'
                z = 0
    return out