def reference(vectors):
    state = 'START'
    carry = {'areset': 0, 'x': 0}
    out = []
    for row in vectors:
        inp = {'areset': carry.get('areset', 0), 'x': carry.get('x', 0)}
        if 'areset' in row:
            inp['areset'] = row['areset']
        if 'x' in row:
            inp['x'] = row['x']
        if inp.get('areset', 0) == 1:
            state = 'START'
        if inp.get('areset', 0) == 1:
            z = 0
            state = 'START'
        else:
            x = inp.get('x', 0)
            if state == 'START':
                if x == 1:
                    state = 'INV1'
                else:
                    state = 'START'
            elif state == 'INV0':
                if x == 0:
                    state = 'INV1'
                else:
                    state = 'INV0'
            else:
                if x == 1:
                    state = 'INV0'
                else:
                    state = 'INV1'
            if state == 'INV1':
                z = 1
            else:
                z = 0
        out.append({'z': z})
        cur = {'areset': inp.get('areset', 0), 'x': inp.get('x', 0)}
        mid = row.get('mid', {})
        if mid:
            if 'areset' in mid:
                cur['areset'] = mid['areset']
            if 'x' in mid:
                cur['x'] = mid['x']
        carry = cur
        if cur.get('areset', 0) == 1:
            state = 'START'
    return out