def reference(vectors):
    # State: out is 32-bit sticky capture; prev_in is previous sampled input
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    MASK = 0xFFFFFFFF
    results = []

    for row in vectors:
        # Drive row's explicit input values before the sampled posedge
        cur_reset = row.get("reset", cur_reset)
        cur_in = row.get("in", cur_in)

        reset = cur_reset
        inp = cur_in & MASK

        # R_RESET: active high synchronous reset clears out.
        # Candidate interpretation: reset also clears/disables previous input history.
        if reset:
            out = 0
            prev_in = 0
        else:
            # R_FALL: set bits where previous input was 1 and current input is 0.
            fall = prev_in & (~inp) & MASK
            # R_HOLD: all other out bits hold their prior value.
            out = (out | fall) & MASK
            # prev_in updates after sampling on non-reset posedge.
            prev_in = inp

        # Output is visible same cycle after posedge.
        results.append({"out": out})

        # Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        mid = row.get("mid", None)
        if mid is not None:
            if "reset" in mid:
                cur_reset = mid["reset"]
            if "in" in mid:
                cur_in = mid["in"] & MASK

    return results
