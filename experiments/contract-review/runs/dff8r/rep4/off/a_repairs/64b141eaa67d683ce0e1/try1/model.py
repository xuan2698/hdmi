def reference(vectors):
    # State: q_reg holds the 8-bit flip-flop output register (R1_sync_reset, R2_dff_capture)
    q_reg = 0  # power-up unspecified; concrete value chosen as 0
    out = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1
        # Sample at posedge clk: outputs reflect current q_reg (visible next_cycle)
        out.append({"q": q_reg & 0xFF})
        # R1_sync_reset: active high synchronous reset sets output to zero on posedge
        if reset == 1:
            q_reg = 0
        else:
            # R2_dff_capture: capture d on posedge when reset == 0
            q_reg = d & 0xFF
    return out
