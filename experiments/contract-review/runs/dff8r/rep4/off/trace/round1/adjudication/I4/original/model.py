def reference(vectors):
    # Contract implementation.
    # State: q_reg (8-bit), updated at posedge clk.
    # R1_sync_reset: reset==1 at posedge -> q_reg <= 0 (priority 1)
    # R2_dff_capture: reset==0 at posedge -> q_reg <= d (priority 2)
    # Outputs sampled after posedge settles; each row's inputs driven before sampled edge.
    # Mid changes occur AFTER sampling, before other edge, carried to start of next row.
    # Power-up unspecified: use 0 as concrete initial value.

    q_reg = 0  # R2_dff_capture (initial state, concrete)

    results = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # Sample after posedge has settled: apply edge update based on current inputs.
        # R1_sync_reset: priority 1
        if reset == 1:
            q_reg = 0
        else:
            # R2_dff_capture: priority 2
            q_reg = d & 0xFF

        results.append({'q': q_reg & 0xFF})

    return results
