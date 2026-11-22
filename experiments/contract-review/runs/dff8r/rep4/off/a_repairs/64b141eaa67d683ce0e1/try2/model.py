def reference(vectors):
    # State: q_reg holds the 8-bit flip-flop output register.
    # R1_sync_reset: on posedge clk, if reset==1, q_reg <= 0 (priority 1).
    # R2_dff_capture: on posedge clk, if reset==0, q_reg <= d (priority 2).
    # Outputs are sampled after the posedge has settled (next_cycle visibility).
    # Mid input changes occur AFTER sampling, before the other edge, and are
    # carried to the start of the next row.
    q_reg = 0  # power-up unspecified; concrete value chosen
    results = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1
        # posedge clk: apply rules with priority
        if reset == 1:  # R1_sync_reset
            q_reg = 0
        else:  # R2_dff_capture
            q_reg = d
        # sample after posedge settled
        results.append({"q": q_reg & 0xFF})
    return results
