def reference(vectors):
    q = 0
    prev_clk = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        if clk == 1 and prev_clk == 0:
            if a == 1:
                q = 4
            else:
                if q == 6:
                    q = 0
                else:
                    q = q + 1
        prev_clk = clk
        out.append({'q': q})
    return out
