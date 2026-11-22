def reference(vectors):
    # Contract implementation.
    # State: q_state (8-bit registered output), initial value unspecified.
    # We model it as 0 for concreteness (power-up unspecified per contract).
    q_state = 0

    results = []

    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1

        # R1_sync_reset: active high synchronous reset -> q = 0 on posedge
        # R2_dff_capture: reset == 0 -> q = d on posedge
        # Both are synchronous, visible same cycle (at the sampled posedge).
        if reset == 1:
            q_state = 0
        else:
            q_state = d

        # Output reflects registered value after the sampled posedge.
        results.append({'q': q_state & 0xFF})

        # Mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row. Since our model
        # only samples at posedge, mid changes do not alter q_state here;
        # they simply become the inputs for the next row (handled by the
        # next iteration reading row values). No action needed.

    return results
