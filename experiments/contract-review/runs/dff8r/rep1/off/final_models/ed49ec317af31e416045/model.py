def reference(vectors):
    # Contract implementation for 8 D flip-flops with active-high synchronous reset.
    # State: q_state (8-bit), initial value unspecified -> we model as 0 for concreteness.
    # Timing: sample inputs at posedge clk; mid changes occur AFTER sampling and carry to next row.

    # R1_sync_reset / R2_dff_capture: state update at posedge clk
    q_state = 0  # initial value before any posedge clk is unspecified; concrete choice = 0

    results = []
    for row in vectors:
        d = row["d"] & 0xFF
        reset = row["reset"] & 0x1

        # --- posedge clk sampling ---
        # R1_sync_reset: reset == 1 -> q <= 0 (priority 1)
        # R2_dff_capture: reset == 0 -> q <= d (priority 2)
        if reset == 1:
            q_state = 0
        else:
            q_state = d

        # Output visible same cycle as the sampled edge
        results.append({"q": q_state & 0xFF})

        # Mid changes (if any) occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row. Since the contract
        # provides no explicit mid-change fields in the row schema, nothing
        # to apply here; the next row's inputs are used as-is.

    return results
