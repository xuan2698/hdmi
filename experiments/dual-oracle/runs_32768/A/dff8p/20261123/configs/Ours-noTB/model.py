def reference(vectors):
    q = 0
    prev_clk = None
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        d = row.get('d', 0) & 255
        reset = row.get('reset', 0)
        if prev_clk == 1 and clk == 0:
            q = 0x34 if reset else d
        out.append({'q': q & 255})
        prev_clk = clk
    return out
