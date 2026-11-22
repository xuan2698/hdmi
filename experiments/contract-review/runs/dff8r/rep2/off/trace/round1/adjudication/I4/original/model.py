def reference(vectors):
    # State: q_state holds the registered 8-bit output value.
    # Initial value is unspecified at power-up; we use 0 as a concrete placeholder.
    q_state = 0

    results = []
    for row in vectors:
        d = row["d"]
        reset = row["reset"]

        # R1_sync_reset: active high synchronous reset sets q to 0 on posedge.
        # R2_dff_capture: when reset == 0, q captures d on posedge.
        # Both rules are evaluated at the posedge; reset has priority.
        if reset == 1:
            q_state = 0  # R1_sync_reset
        else:
            q_state = d & 0xFF  # R2_dff_capture

        # Output visible same cycle after the sampled posedge.
        results.append({"q": q_state})

    return results
