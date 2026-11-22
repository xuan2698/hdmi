def reference(vectors):
    # Contract implementation for 8 D flip-flops with active-high synchronous reset.
    # State: q_reg holds the 8-bit output; unspecified before first posedge.
    # R1_sync_reset: on posedge clk with reset==1, q_reg <- 0 (priority 1).
    # R2_dff_capture: on posedge clk with reset==0, q_reg <- d (priority 2).
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.

    q_reg = 0  # unspecified power-up; concrete value chosen for determinism
    results = []

    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1

        # Sample at posedge clk (edge has settled).
        # R1_sync_reset (priority 1): reset==1 -> q_reg = 0
        # R2_dff_capture (priority 2): reset==0 -> q_reg = d
        if reset == 1:
            q_reg = 0
        else:
            q_reg = d

        # Output visible next cycle (after posedge).
        results.append({"q": q_reg & 0xFF})

        # Mid input changes (if any) occur AFTER sampling, before other edge,
        # carried to start of next row. Since inputs are per-row dicts, the
        # next row's values already reflect any mid changes; nothing to do here.

    return results
