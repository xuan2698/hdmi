def reference(vectors):
    q = 0
    prev_clk = 0
    out = []
    for v in vectors:
        if 'clk' in v:
            clk = v['clk']
            if clk == 1 and prev_clk == 0:
                if v['reset'] == 1:
                    q = 0
                else:
                    q = (q + 1) % 10
            prev_clk = clk
        else:
            if v['reset'] == 1:
                q = 0
            else:
                q = (q + 1) % 10
        out.append({'q': q})
    return out
