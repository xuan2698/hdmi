def reference(vectors):
    s = 0
    prev_clk = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        b = row.get('b', 0)
        q = (a ^ b ^ s) & 1
        out.append({'q': q, 'state': s})
        if prev_clk == 1 and clk == 0:
            s = ((a & b) | (a & s) | (b & s)) & 1
        prev_clk = clk
    return out
