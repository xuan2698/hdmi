def reference(vectors):
    # Initial concrete state (power-up unspecified; choose 0 for out and prev_in).
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    MASK = (1 << 32) - 1
    result = []

    for row in vectors:
        # Drive row inputs before the sampled posedge; explicit row values override carried mid values.
        if "reset" in row:
            cur_reset = row["reset"]
        if "in" in row:
            cur_in = row["in"]

        in_val = cur_in & MASK

        # rule reset_clear: synchronous active-high reset has priority; out becomes 0.
        if cur_reset == 1:
            out = 0
            # prev_in tracks in on every posedge including reset cycles.
            # capture_fall uncertain: current-contract behavior allows reset-cycle in=1 to pair with later in=0.
            prev_in = in_val
        else:
            # rule capture_fall: per-bit detect previous sampled 1 to current sampled 0.
            fall = prev_in & ((~in_val) & MASK)
            # rule hold_state: out holds except where a falling edge was captured.
            out = (out | fall) & MASK
            prev_in = in_val

        # Output visible same cycle after posedge.
        result.append({"out": out})

        # Apply optional mid changes AFTER sampling; they become start values for the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "reset" in mid:
                    cur_reset = mid["reset"]
                if "in" in mid:
                    cur_in = mid["in"]

    return result
