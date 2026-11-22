def reference(vectors):
    # State: out (32-bit sticky flag), prev_in (previous sampled input)
    out = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        inp = row.get('in', 0) & 0xFFFFFFFF
        # R1_reset_clear: synchronous reset clears out on posedge (priority 1)
        if reset == 1:
            out = 0
        else:
            # R2_capture_falling: set sticky bits where prev_in bit was 1 and current in bit is 0
            falling = prev_in & (~inp) & 0xFFFFFFFF
            out = (out | falling) & 0xFFFFFFFF
            # R3_hold: bits without falling transition remain unchanged (implicit in OR)
        # Sample output visible this cycle (after posedge settles)
        results.append({'out': out & 0xFFFFFFFF})
        # Update prev_in for next cycle (mid changes carried to start of next row)
        prev_in = inp
    return results
