def reference(vectors):
    q = 0
    cur = {'d': 0, 'r': 0}
    out = []
    for row in vectors:
        for k in ('d', 'r'):
            if k in row:
                cur[k] = row[k]
        q = 0 if cur.get('r', 0) else (cur.get('d', 0) & 1)
        out.append({'q': q})
        mid = row.get('mid')
        if isinstance(mid, dict):
            for k, v in mid.items():
                if k in ('d', 'r'):
                    cur[k] = v
    return out
