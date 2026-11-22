def reference(vectors):
    # Contract implementation for a 1-bit D flip-flop with active-high synchronous reset.
    # State: Q (stored flip-flop value, driven to q). Updates on posedge clk.
    # Power-up value is unspecified; we choose 0 as a concrete initial value.
    Q = 0  # named state: stored flip-flop value

    out = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # R1: r == 1 -> synchronous reset, q = 0 (priority 1)
        # R2: r == 0 -> D flip-flop, q = d (priority 2)
        # Both rules are visible same_cycle at posedge clk.
        if r == 1:
            Q = 0  # R1
        else:
            Q = d  # R2

        # Mid input changes occur AFTER sampling; they are carried to the
        # start of the next row, so we do not apply them to this row's output.
        out.append({'q': Q & 1})

    return out
