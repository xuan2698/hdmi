def reference(vectors):
    state = 0
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        clk = row.get('clk', 0)
        if clk == 1:
            nxt = (a & b) ^ state
            q = nxt
            state = nxt
        out.append({'q': q, 'state': state})
        mid = row.get('mid')
        if mid:
            a = mid.get('a', a)
            b = mid.get('b', b)
            if mid.get('clk', clk) == 1:
                nxt = (a & b) ^ state
                q = nxt
                state = nxt
    return out
