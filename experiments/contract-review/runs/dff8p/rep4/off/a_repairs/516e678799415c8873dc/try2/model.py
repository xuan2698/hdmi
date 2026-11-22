def reference(vectors):
    # State: q_reg holds the 8 D flip-flop outputs.
    # Initial value is unspecified at power-up; we choose 0x34 to be concrete.
    q_reg = 0x34

    results = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1

        # R1_sync_reset / R3_reset_value: active-high synchronous reset on negedge clk.
        # Reset value 0x34 becomes visible on q at the negedge where reset==1.
        if reset == 1:
            q_reg = 0x34
        else:
            # R2_dff_capture: capture d on negedge clk when reset==0.
            q_reg = d

        results.append({"q": q_reg & 0xFF})

    return results
