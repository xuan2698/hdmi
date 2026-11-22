def reference(vectors):
    q = 0
    cur = {}
    out = []
    for row in vectors:
        for k in ('d', 'r'):
            if k in row:
                cur[k] = int(row[k])
        if 'd' not in cur:
            cur['d'] = 0
        if 'r' not in cur:
            cur['r'] = 0
        if cur['r'] == 1:
            q = 0
        else:
            q = cur['d']
        out.append({'q': q})
        if 'mid' in row:
            mid = row['mid']
            for k in ('d', 'r'):
                if k in mid:
                    cur[k] = int(mid[k])
    return out