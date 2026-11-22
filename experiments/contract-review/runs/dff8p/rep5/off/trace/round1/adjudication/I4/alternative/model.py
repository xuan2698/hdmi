def reference(vectors):
    # Contract implementation.
    # R1_sync_reset: active high synchronous reset, priority 1, applied at negedge, q <- 0x34.
    # R2_dff_capture: on negedge with reset==0, q <- d.
    # global: q initializes to 0x00 at time zero before any clock edge.
    # mid: mid input changes occur AFTER sampling, before the other edge, carried to next row.
    # Timing: each row's values are driven before the sampled negedge; sample after negedge settles.

    q_state = 0x00  # global: power-up value before any clock edge

    results = []
    for row in vectors:
        d = row.get("d", 0) & 0xFF
        reset = row.get("reset", 0) & 0x1

        # Sample at negedge (values driven before the edge).
        if reset == 1:
            # R1_sync_reset
            q_state = 0x34
        else:
            # R2_dff_capture
            q_state = d

        results.append({"q": q_state & 0xFF})

    return results
