def reference(vectors):
    state = 0
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        clk = row.get('clk', 0)
        if clk == 1:
            nq = (a ^ b) ^ state
            state = nq
            q = nq
        out.append({'q': q, 'state': state})
        mid = row.get('mid')
        if mid:
            if 'a' in mid:
                a = mid['a']
            if 'b' in mid:
                b = mid['b']
    return out
