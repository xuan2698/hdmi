def reference(vectors):
    # Contract:
    # - State Q: stored flip-flop value, driven to q.
    # - Before any posedge clk, Q is unspecified; we initialize to 0.
    # - On posedge clk: if r == 1, Q <= 0 (R1, priority 1, sync reset).
    # - On posedge clk: if r == 0, Q <= d (R2, priority 2).
    # - Mid input changes occur AFTER sampling, before the other edge,
    #   and are carried to the start of the next row.
    # - Each row's values are driven before the sampled edge.
    # - Sample after the posedge edge has settled.

    Q = 0  # R1/R2: unspecified before first posedge; concrete init to 0
    out = []
    for row in vectors:
        d = row["d"] & 1
        r = row["r"] & 1
        # posedge sampling: apply rules by priority
        if r == 1:  # R1: active high synchronous reset
            Q = 0
        else:       # R2: D flip flop load
            Q = d
        out.append({"q": Q & 1})
        # mid changes (if any) occur after sampling; carried to next row.
        # No mid fields in this contract's vectors, so nothing to apply.
    return out
