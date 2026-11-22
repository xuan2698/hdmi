def reference(vectors):
    # State: q_reg holds the 8 D flip-flop outputs.
    # Power-up value is unspecified; we initialize to the reset value 0x34
    # so that the first sampled negedge produces a concrete value.
    q_reg = 0x34

    results = []

    for row in vectors:
        d = row.get("d", 0)
        reset = row.get("reset", 0)

        # R1_sync_reset: active-high synchronous reset on negedge clk.
        # R3_reset_value: reset value is 0x34.
        # R2_dff_capture: otherwise capture d on negedge clk.
        # The negedge is the sampling edge; values are driven before it,
        # so we apply the transition here (visible same_cycle).
        if reset == 1:
            q_reg = 0x34
        else:
            q_reg = d & 0xFF

        # Output visible same cycle after the negedge has settled.
        results.append({"q": q_reg & 0xFF})

        # Mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row. Since we read
        # inputs fresh at the start of each row, mid changes are naturally
        # reflected in the next row's inputs.

    return results
