def reference(vectors):
    # State: out_reg (32-bit sticky flag), prev_in (32-bit previous input), prev_valid
    out_reg = 0
    prev_in = 0
    prev_valid = False

    results = []
    for row in vectors:
        reset = row['reset'] & 1
        inp = row['in'] & 0xFFFFFFFF

        # R1_reset_clear: synchronous reset clears out_reg (priority 1)
        if reset == 1:
            out_reg = 0
            # global interpretation: prev_in not tracked across reset
            prev_valid = False
            prev_in = 0
        else:
            # R2_capture_falling_edge: capture 1->0 transitions (priority 2)
            # global interpretation: first non-reset cycle has no valid prev_in
            if prev_valid:
                falling = prev_in & (~inp & 0xFFFFFFFF)
                out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold_until_reset: otherwise hold (priority 3) - implicit
            prev_in = inp
            prev_valid = True

        results.append({'out': out_reg & 0xFFFFFFFF})

    return results
