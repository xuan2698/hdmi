def reference(vectors):
    # Contract: 8 D flip-flops, posedge clk, active-high synchronous reset.
    # q updates 1 cycle after the sampled posedge. Mid changes occur after
    # sampling and are carried to the start of the next row.
    q = 0  # power-up unspecified; use 0 as concrete value
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        reset = row.get('reset', 0)
        d = row.get('d', 0)
        # Sample on posedge: use current inputs (driven before edge)
        # We model each row as a clock edge event when clk==1.
        if clk == 1:
            if reset == 1:
                q = 0
            else:
                q = d & 0xFF
        out.append({'q': q & 0xFF})
    return out
