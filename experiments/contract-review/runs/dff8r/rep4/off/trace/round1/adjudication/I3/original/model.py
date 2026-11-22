def reference(vectors):
    # R1_sync_reset / R2_dff_capture: state register q_reg, 8-bit, updated on posedge clk.
    # Power-up unspecified -> concrete default 0.
    q_reg = 0

    results = []
    for row in vectors:
        # Sample inputs for this row (driven before the sampled posedge).
        d = row.get("d", 0)
        reset = row.get("reset", 0)

        # Coerce to concrete unsigned ints within bit widths.
        d = int(d) & 0xFF
        reset = int(reset) & 0x1

        # Posedge clk: compute next state.
        # R1_sync_reset: reset == 1 -> q_reg <= 0 (priority 1).
        # R2_dff_capture: reset == 0 -> q_reg <= d (priority 2).
        if reset == 1:
            q_reg = 0
        else:
            q_reg = d

        # Output visible next_cycle: emit q after the sampled edge settles.
        results.append({"q": q_reg & 0xFF})

        # Mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row. No mid handling
        # needed here since inputs are re-read per row.

    return results
