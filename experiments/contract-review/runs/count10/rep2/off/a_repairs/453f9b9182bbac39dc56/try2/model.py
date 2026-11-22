def reference(vectors):
    # Contract implementation for a synchronous active-high reset decade counter.
    # State: COUNT holds current count 0..9.
    # R1_SYNC_RESET: on posedge, if reset==1, q <= 0 (same cycle visible).
    # R2_COUNT_UP_WRAP: on posedge, if reset==0, q <= (q+1) mod 10.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    # Power-up: choose q=0 (selected interpretation for determinism).

    q = 0  # initial state (power-up interpretation: 0)

    results = []
    for row in vectors:
        # Sample inputs for this row (driven before the sampled posedge).
        reset = row.get("reset", 0)

        # Compute next state at posedge (synchronous).
        # R1_SYNC_RESET (priority 1)
        if reset == 1:
            q_next = 0
        else:
            # R2_COUNT_UP_WRAP (priority 2)
            q_next = (q + 1) % 10

        # Output visible same cycle after edge settles.
        q = q_next
        results.append({"q": q & 0xF})

        # Mid changes occur AFTER sampling; they are carried to the start of
        # the next row. Since we read inputs per-row from the vector, mid
        # changes are already represented in the next row's inputs.

    return results
