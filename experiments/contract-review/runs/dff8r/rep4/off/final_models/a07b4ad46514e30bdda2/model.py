def reference(vectors):
    # Contract implementation.
    # State: q_reg holds the 8-bit flip-flop output. Initial value unspecified;
    # we model it as 0 (example assumption) but every returned row is concrete.
    q_reg = 0

    results = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1

        # R1_sync_reset: on posedge clk, if reset==1, q <= 0 (priority 1).
        # R2_dff_capture: on posedge clk, if reset==0, q <= d (priority 2).
        # Both are synchronous, visible next_cycle. We sample the current row's
        # inputs at the posedge, then produce the next-cycle output.
        if reset == 1:
            q_reg = 0  # R1_sync_reset
        else:
            q_reg = d  # R2_dff_capture

        # Mid changes occur AFTER sampling and are carried to the next row;
        # they do not affect this row's sampled output.
        results.append({"q": q_reg & 0xFF})

    return results
