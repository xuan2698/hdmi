def reference(vectors):
    # State: out (32-bit sticky), prev_in (32-bit previous input)
    # R2_capture_falling: prev_in initialized to 0 before first sampled posedge
    out = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        inp = row.get('in', 0) & 0xFFFFFFFF
        # R1_reset_clear: synchronous reset clears out (priority 1)
        if reset == 1:
            out = 0
        else:
            # R2_capture_falling: capture 1->0 transitions
            falling = prev_in & (~inp & 0xFFFFFFFF)
            out = out | falling
            # R3_hold: out unchanged when no falling transitions (implicit)
        results.append({'out': out & 0xFFFFFFFF})
        # Update prev_in after sampling (mid changes carried to next row start)
        prev_in = inp
    return results
