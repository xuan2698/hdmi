def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit sticky flag), prev_in (32-bit previous input).
    # Power-up: unspecified; we choose 0 for out_reg and prev_in.
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row['reset'] & 1
        inp = row['in'] & 0xFFFFFFFF
        # R1_reset_clear: synchronous active-high reset clears out_reg at posedge.
        if reset == 1:
            out_reg = 0
        else:
            # R2_capture_falling: capture 1->0 transitions of in.
            falling = prev_in & (~inp) & 0xFFFFFFFF
            out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold: otherwise out_reg holds its value (no change).
        # Update prev_in for next cycle (mid changes carried to next row start).
        prev_in = inp
        results.append({'out': out_reg & 0xFFFFFFFF})
    return results
