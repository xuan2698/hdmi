def reference(vectors):
    # State: out is the 32-bit sticky capture register; prev_in is the previous sampled input.
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    result = []
    for row in vectors:
        # Start-of-row values from carried mid changes, explicitly overridden by row values.
        if "reset" in row:
            cur_reset = row["reset"]
        if "in" in row:
            cur_in = row["in"]

        # reset_clear: active-high synchronous reset has priority and clears out on posedge.
        if cur_reset:
            out = 0
        else:
            # capture_fall: per-bit 1-to-0 detected from prev_in to cur_in.
            fall = prev_in & (~cur_in) & 0xFFFFFFFF
            # hold_state: non-falling bits hold previous out; falling bits become 1.
            out = (out | fall) & 0xFFFFFFFF

        # prev_in tracks in on every posedge, including reset cycles.
        prev_in = cur_in & 0xFFFFFFFF

        # Same-cycle visible output after the sampled posedge.
        result.append({"out": out})

        # mid changes occur after sampling and are carried to the start of the next row.
        if "mid" in row and row["mid"] is not None:
            md = row["mid"]
            if "reset" in md:
                cur_reset = md["reset"]
            if "in" in md:
                cur_in = md["in"]

    return result
