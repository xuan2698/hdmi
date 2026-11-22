def reference(vectors):
    # State: q_reg holds the 8 D flip-flop outputs.
    # Initial value is unspecified at power-up; we choose 0x34 to be concrete.
    q_reg = 0x34

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1_sync_reset / R3_reset_value: on negedge clk, if reset==1, q <= 0x34.
        # R2_dff_capture: on negedge clk, if reset==0, q <= d.
        # The sampled edge is the negedge; values are driven before it.
        if reset == 1:
            q_reg = 0x34
        else:
            q_reg = d

        results.append({'q': q_reg & 0xFF})

    return results
