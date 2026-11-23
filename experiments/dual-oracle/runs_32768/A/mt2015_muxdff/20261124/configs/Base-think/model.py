def reference(vectors):
    Q = 0
    cur = {'L': 0, 'q_in': 0, 'r_in': 0}
    out = []
    for row in vectors:
        for k in ('L', 'q_in', 'r_in'):
            if k in row:
                cur[k] = int(row[k]) & 1
        L = cur['L']
        q_in = cur['q_in']
        r_in = cur['r_in']
        Q = (r_in if L else q_in) & 1
        out.append({'Q': Q})
        mid = row.get('mid')
        if mid:
            for k, v in mid.items():
                if k in cur:
                    cur[k] = int(v) & 1
    return out
