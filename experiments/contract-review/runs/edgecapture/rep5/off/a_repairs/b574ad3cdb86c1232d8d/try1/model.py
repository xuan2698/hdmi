def reference(vectors):
    # State: out (32-bit sticky flag), prev_in (32-bit previous input)
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
            # R2_capture_falling: set bits where prev_in=1 and in=0
            falling = prev_in & (~inp) & 0xFFFFFFFF
            out = (out | falling) & 0xFFFFFFFF
            # R3_hold: bits without falling transition keep previous value (implicit)
        results.append({'out': out & 0xFFFFFFFF})
        # Update prev_in for next cycle (mid changes carried to next row start)
        prev_in = inp
    return results
