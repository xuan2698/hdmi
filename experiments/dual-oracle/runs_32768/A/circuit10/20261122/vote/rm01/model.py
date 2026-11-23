def reference(vectors):
    state = 0
    out = []
    prev_clk = 0
    prev_a = 0
    prev_b = 0
    first = True
    for v in vectors:
        if 'clk' in v:
            clk = int(v['clk']) & 1
            a = int(v['a']) & 1
            b = int(v['b']) & 1
            if clk and not prev_clk:
                if first:
                    if a == b:
                        state = a
                else:
                    if prev_a == prev_b:
                        state = prev_a
            q = state ^ a ^ b
            out.append({'q': q & 1, 'state': state & 1})
            prev_clk = clk
            prev_a = a
            prev_b = b
            first = False
        else:
            a = int(v['a']) & 1
            b = int(v['b']) & 1
            if a == b:
                state = a
            q = state ^ a ^ b
            out.append({'q': q & 1, 'state': state & 1})
            first = False
    return out
