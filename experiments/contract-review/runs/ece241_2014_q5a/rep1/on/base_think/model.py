def reference(vectors):
    state = 0
    cur = {'areset': 0, 'x': 0}
    out = []
    for row in vectors:
        for k in ('areset', 'x'):
            if k in row:
                cur[k] = int(row[k])
        if cur['areset']:
            state = 0
        else:
            x = cur['x']
            if state == 0:
                state = 1 if x else 0
            else:
                state = 1 if not x else 2
        out.append({'z': 1 if state == 1 else 0})
        mid = row.get('mid')
        if mid:
            for k, v in mid.items():
                if k in ('areset', 'x'):
                    cur[k] = int(v)
                    if k == 'areset' and cur[k]:
                        state = 0
    return out
