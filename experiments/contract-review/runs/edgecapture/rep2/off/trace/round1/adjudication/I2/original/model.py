def reference(vectors):
    # State: out_reg (32-bit sticky flag), prev_in (32-bit previous input)
    # R1_reset_clear: sync active-high reset clears out_reg at posedge
    # R2_capture_falling: set bits where prev_in & ~in at posedge (reset==0)
    # R3_hold: otherwise hold out_reg
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row['reset'] & 1
        cur_in = row['in'] & 0xFFFFFFFF
        # R1_reset_clear: reset has priority 0
        if reset == 1:
            out_reg = 0
        else:
            # R2_capture_falling: priority 1
            falling = prev_in & (~cur_in & 0xFFFFFFFF)
            if falling != 0:
                out_reg = out_reg | falling
            # R3_hold: priority 2 (no change)
        # Output visible same cycle for reset, next cycle for capture/hold
        results.append({'out': out_reg & 0xFFFFFFFF})
        # Update prev_in for next cycle (mid changes carried to next row start)
        prev_in = cur_in
    return results
