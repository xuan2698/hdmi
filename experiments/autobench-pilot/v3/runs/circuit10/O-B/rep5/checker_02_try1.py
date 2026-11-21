def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        clk = row.get('clk', 0)
        if clk == 1:
            state = (a ^ b) & 1
        q = state
        out.append({'q': q, 'state': state})
        if 'mid' in row:
            m = row['mid']
            a = m.get('a', a)
            b = m.get('b', b)
            if m.get('clk', 0) == 1:
                state = (a ^ b) & 1
    return out
