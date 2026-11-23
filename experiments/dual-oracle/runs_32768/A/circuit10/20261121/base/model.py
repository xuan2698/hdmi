def reference(vectors):
    state = 0
    prev_clk = 0
    a = 0
    b = 0
    result = []
    for row in vectors:
        clk = row.get('clk', prev_clk)
        a = row.get('a', a)
        b = row.get('b', b)
        if clk == 1 and prev_clk == 0:
            state = (a & b) | (a & state) | (b & state)
        q = a ^ b ^ state
        result.append({'q': int(q), 'state': int(state)})
        if 'mid' in row:
            mid = row['mid']
            a = mid.get('a', a)
            b = mid.get('b', b)
            clk = mid.get('clk', clk)
        prev_clk = clk
    return result
