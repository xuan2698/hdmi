def reference(vectors):
    s = 0
    cur = {'in': 0, 'reset': 0}
    r = []
    for row in vectors:
        for k, v in row.items():
            if k != 'mid':
                cur[k] = v
        if cur.get('reset', 0):
            s = 0
        else:
            i = cur.get('in', 0)
            if s == 0:
                s = 0 if i == 0 else 1
            elif s == 1:
                s = 2 if i == 0 else 1
            elif s == 2:
                s = 0 if i == 0 else 3
            else:
                s = 2 if i == 0 else 1
        r.append({'out': 1 if s == 3 else 0})
        if 'mid' in row:
            for k, v in row['mid'].items():
                cur[k] = v
    return r
