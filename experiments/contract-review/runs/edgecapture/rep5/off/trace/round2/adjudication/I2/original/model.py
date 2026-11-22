def reference(vectors):
    # Contract implementation.
    # State: out (32-bit sticky flag), prev_in (32-bit previous sampled input).
    # R1_reset_clear: on posedge with reset==1, out cleared to 0 (same_cycle visible).
    # R2_capture_falling: on posedge with reset==0, out |= prev_in & ~in (next_cycle visible).
    # R3_hold: on posedge with reset==0 and no falling edges, out unchanged.
    # prev_in initialized to 0 before first sampled cycle.
    # Mid changes occur AFTER sampling, carried to start of next row.

    out = 0
    prev_in = 0
    results = []

    for row in vectors:
        reset = row.get("reset", 0) & 1
        in_val = row.get("in", 0) & 0xFFFFFFFF

        # Sample at posedge: compute next state based on current inputs and prev_in.
        if reset == 1:
            # R1_reset_clear
            new_out = 0
        else:
            # R2_capture_falling and R3_hold
            falling = prev_in & (~in_val & 0xFFFFFFFF)
            new_out = (out | falling) & 0xFFFFFFFF

        # Output visible for this row (same_cycle for reset, next_cycle for capture).
        # Per contract, out reflects the state after this posedge.
        out = new_out
        results.append({"out": out & 0xFFFFFFFF})

        # Update prev_in to the sampled input for next cycle.
        prev_in = in_val

    return results
