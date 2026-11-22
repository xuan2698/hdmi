def reference(vectors):
    # Contract implementation.
    # State: q_state (8-bit registered output), initial value unspecified.
    # We model it as 0 before first posedge (concrete value required in output).
    q_state = 0

    results = []
    for row in vectors:
        d = row["d"]
        reset = row["reset"]

        # R1_sync_reset: active high synchronous reset -> q = 0 on posedge, priority 1
        # R2_dff_capture: reset == 0 -> q = d on posedge, priority 2
        # Both rules update at posedge clk (sampled edge has settled).
        if reset == 1:
            q_state = 0  # R1_sync_reset
        else:
            q_state = d & 0xFF  # R2_dff_capture

        # Output visible same cycle after posedge.
        results.append({"q": q_state})

    return results
