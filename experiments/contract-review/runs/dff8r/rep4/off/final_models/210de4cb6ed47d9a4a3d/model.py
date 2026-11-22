def reference(vectors):
    # State: q_reg holds the 8-bit flip-flop output register (R1_sync_reset, R2_dff_capture)
    q_reg = 0  # power-up unspecified; concrete value chosen as 0
    out = []
    for row in vectors:
        # Sample inputs at posedge clk (values driven before the sampled edge)
        d = row['d'] & 0xFF
        reset = row['reset'] & 0x1
        # R1_sync_reset: active high synchronous reset -> q = 0 on posedge, priority 1
        if reset == 1:
            q_reg = 0
        else:
            # R2_dff_capture: capture d on posedge when reset == 0, priority 2
            q_reg = d
        # Output visible next_cycle
        out.append({'q': q_reg & 0xFF})
        # Mid input changes occur AFTER sampling; carried to start of next row.
        # (No mid changes modeled here; inputs are re-read from next row.)
    return out
