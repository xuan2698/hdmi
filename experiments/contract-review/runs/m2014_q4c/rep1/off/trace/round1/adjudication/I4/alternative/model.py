def reference(vectors):
    # State: Q = stored flip-flop value, driven to q
    # Power-up unspecified -> use 0 as concrete initial value
    Q = 0

    # R1_sync_reset (candidate interpretation): reset output becomes 0 one cycle
    # after the posedge with r=1 (registered reset). So on a posedge with r=1,
    # Q is scheduled to become 0, visible on the NEXT cycle's output.
    # R2_capture_d: on posedge with r=0, Q captures d, visible same cycle.

    # We model a "pending reset" flag: when a posedge with r=1 occurs, the
    # output for the *next* row must be 0 (registered reset), overriding capture.
    pending_reset = False

    results = []
    for row in vectors:
        d = row['d'] & 1
        r = row['r'] & 1

        # Determine output for this row based on state established at the
        # previous posedge (sampled edge already settled).
        if pending_reset:
            # R1_sync_reset: registered reset takes effect this cycle
            Q = 0
            pending_reset = False

        # Output for this row reflects current Q (post previous-edge update)
        results.append({'q': Q & 1})

        # At this row's posedge (sampling edge), compute next state.
        # Mid changes occur AFTER sampling, so they don't affect this edge.
        if r == 1:
            # R1_sync_reset: schedule registered reset for next cycle
            pending_reset = True
        else:
            # R2_capture_d: capture d, visible same cycle (next row)
            Q = d

    return results
