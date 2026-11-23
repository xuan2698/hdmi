def reference(vectors):
    q = 0
    cur = {'clk': 0, 'a': 0}
    prev = 0
    out = []
    for v in vectors:
        for k, val in v.items():
            if k != 'mid':
                cur[k] = val
        clk = cur.get('clk', 0)
        a = cur.get('a', 0)
        if prev == 0 and clk == 1:
            if a:
                q = 4
            else:
                q = 0 if q == 6 else q + 1
        out.append({'q': q})
        if 'mid' in v:
            for k, val in v['mid'].items():
                cur[k] = val
        prev = clk
    return out
