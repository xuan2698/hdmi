def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        if row.get('clk', 0) == 1:
            nxt = (a ^ b) ^ state
            state = nxt
        q = state
        out.append({'q': q, 'state': state})
        if 'mid' in row:
            m = row['mid']
            a = m.get('a', a)
            b = m.get('b', b)
    return out
