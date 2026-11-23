def reference(vectors):
    q = 0
    prev_clk = 0
    out = []
    for row in vectors:
        if 'clk' in row:
            clk = int(row['clk']) & 1
            posedge = prev_clk == 0 and clk == 1
            prev_clk = clk
        else:
            posedge = True

        if posedge:
            reset = int(row.get('reset', 0)) & 1
            if reset:
                q = 0
            else:
                q = (q + 1) % 10

        out.append({'q': q})

    return out
