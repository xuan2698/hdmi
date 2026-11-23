def reference(vectors):
    state = 0
    prev_clk = 0
    prev_a = 0
    prev_b = 0
    have_prev = False
    out = []
    for row in vectors:
        a = int(row.get('a', 0)) & 1
        b = int(row.get('b', 0)) & 1
        if 'clk' in row:
            clk = int(row.get('clk', 0)) & 1
        elif 'CLK' in row:
            clk = int(row.get('CLK', 0)) & 1
        else:
            clk = None
        if clk is None:
            state = (a & b) | (state & (a | b))
        else:
            if clk == 1 and prev_clk == 0:
                if have_prev:
                    sa = prev_a
                    sb = prev_b
                else:
                    sa = a
                    sb = b
                state = (sa & sb) | (state & (sa | sb))
            prev_clk = clk
        q = (a ^ b ^ state) & 1
        out.append({'q': q, 'state': state})
        prev_a = a
        prev_b = b
        have_prev = True
    return out
