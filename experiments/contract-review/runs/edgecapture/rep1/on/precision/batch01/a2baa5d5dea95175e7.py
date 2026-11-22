def reference(vectors):
    # R_RESET: synchronous reset clears out to 0 with priority.
    # R_FALL: set out bits for 1-to-0 transitions using prev_in.
    # R_HOLD: out holds its prior value when no reset or fall.
    # I1 chosen assumption: prev_in updates on every posedge including reset.
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    result = []
    for row in vectors:
        # Apply row's driven values before the sampled edge.
        if "reset" in row:
            cur_reset = row["reset"]
        if "in" in row:
            cur_in = row["in"]
        cur_in = cur_in & 0xFFFFFFFF

        # Synchronous sampling at posedge.
        if cur_reset:  # R_RESET
            out = 0
        else:
            # R_FALL
            fall = prev_in & (0xFFFFFFFF ^ cur_in)
            out = out | fall
        # R_HOLD is implicit by not clearing out when neither reset nor fall occurs.
        out = out & 0xFFFFFFFF

        # prev_in updates on every posedge including reset (I1 assumption).
        prev_in = cur_in

        result.append({"out": out})

        # Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "reset" in mid:
                    cur_reset = mid["reset"]
                if "in" in mid:
                    cur_in = mid["in"]

    return result
