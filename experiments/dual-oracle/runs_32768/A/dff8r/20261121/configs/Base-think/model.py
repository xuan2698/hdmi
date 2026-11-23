def reference(vectors):
    q = 0
    inp = {'d': 0, 'reset': 0}
    out = []
    for row in vectors:
        for k in ('d', 'reset'):
            if k in row:
                inp[k] = row[k]
        if inp.get('reset', 0):
            q = 0
        else:
            q = inp.get('d', 0) & 0xFF
        out.append({'q': q})
        mid = row.get('mid')
        if isinstance(mid, dict):
            for k, v in mid.items():
                if k in ('d', 'reset'):
                    inp[k] = v
    return out
