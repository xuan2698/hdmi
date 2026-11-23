def reference(vectors):
    state = 0
    start = 0
    cur = {'reset': 0, 'data': 0}
    out = []
    for row in vectors:
        for k in ('reset', 'data'):
            if k in row:
                cur[k] = row[k]
        r = cur.get('reset', 0)
        d = cur.get('data', 0)
        if r:
            state = 0
            start = 0
        elif not start:
            if state == 0:
                state = 1 if d else 0
            elif state == 1:
                state = 2 if d else 0
            elif state == 2:
                state = 2 if d else 3
            else:
                if d:
                    start = 1
                    state = 4
                else:
                    state = 0
        out.append({'start_shifting': start})
        if 'mid' in row:
            for k, v in row['mid'].items():
                if k in ('reset', 'data'):
                    cur[k] = v
    return out
