def reference(vectors):
    out = 0
    prev = 0
    prev_clk = 0
    result = []
    for row in vectors:
        if 'clk' in row:
            clk = int(row['clk']) & 1
            posedge = (prev_clk == 0 and clk == 1)
            prev_clk = clk
        else:
            posedge = True
        if posedge:
            if int(row.get('reset', 0)) & 1:
                out = 0
                prev = 0
            else:
                x = int(row.get('in', 0)) & 0xFFFFFFFF
                out = (out | (prev & (~x & 0xFFFFFFFF))) & 0xFFFFFFFF
                prev = x
        result.append({'out': out & 0xFFFFFFFF})
    return result
