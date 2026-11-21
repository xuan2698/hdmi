def reference(vectors):
    state = 0
    q = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        b = row.get('b', 0)
        if clk == 1:
            nq = (a & b) ^ state
            state = nq
            q = nq
        out.append({'q': q & 1, 'state': state & 1})
        if 'mid' in row:
            m = row['mid']
            if 'a' in m: a = m['a']
            if 'b' in m: b = m['b']
    return out
