def reference(vectors):
    # D flip-flop with active-high synchronous reset.
    # Each row: inputs are driven before the sampled posedge.
    # q updates on posedge: q <= 0 if r else d.
    # Mid changes occur after sampling, before next edge; carried to next row start.
    # Power-up: q unspecified -> use 0 as concrete value.
    q = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        d = row.get('d', 0)
        r = row.get('r', 0)
        # Sample on posedge (clk transitions 0->1). We treat each row as
        # containing a posedge sample point; apply update.
        if clk == 1:
            if r == 1:
                q = 0
            else:
                q = d & 1
        out.append({'q': q & 1})
    return out
