def reference(vectors):
    # Contract implementation for 32-bit falling-edge (1->0) sticky capture.
    # State: out (32-bit sticky flags), prev_in (32-bit previous sampled input).
    # Timing: sample at posedge clk; mid changes occur after sampling and
    # carry to the start of the next row.

    MASK = 0xFFFFFFFF

    # Power-up: unspecified, but must return concrete values. Start at 0.
    out = 0
    prev_in = 0

    results = []

    for row in vectors:
        reset = row.get("reset", 0) & 1
        # Mid changes from previous row are already reflected in row["in"].
        in_val = row.get("in", 0) & MASK

        # R1_reset_clear: synchronous active-high reset clears out on posedge.
        if reset == 1:
            out = 0
        else:
            # R2_capture_falling: set sticky bit where prev_in=1 and in=0.
            falling = prev_in & (~in_val & MASK)
            out = (out | falling) & MASK
            # R3_hold: bits without a falling transition retain their value
            # (implicitly handled by OR above).

        # Update previous input for next cycle's edge detection.
        prev_in = in_val

        results.append({"out": out & MASK})

    return results
