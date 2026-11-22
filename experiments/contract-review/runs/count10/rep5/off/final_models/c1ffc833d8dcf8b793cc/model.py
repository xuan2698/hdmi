def reference(vectors):
    # Contract implementation for a synchronous active-high-reset decade counter.
    # State: COUNT (4-bit q). Reset is synchronous and sampled on posedge clk.
    # Each row: inputs are driven before the sampled posedge; outputs are
    # reported as the value visible after that posedge settles.
    # Mid changes occur AFTER sampling and are carried to the next row.

    q = 0  # power-up state (unspecified in spec; choose 0 as concrete value)

    results = []
    for row in vectors:
        # Determine reset value for this row's sampled edge.
        # A mid change from the previous row may have updated reset; the
        # caller passes the effective value for this row in 'reset'.
        reset = row.get("reset", 0)

        # R1: reset == 1 -> synchronous reset to 0 on posedge (priority 1)
        if reset == 1:
            q = 0
        # R2: reset == 0 && q < 9 -> increment on posedge (priority 2)
        elif q < 9:
            q = q + 1
        # R3: reset == 0 && q == 9 -> wrap to 0 on posedge (priority 3)
        else:  # q == 9
            q = 0

        # Output visible same cycle after the posedge settles.
        results.append({"q": q & 0xF})

    return results
