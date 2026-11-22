def reference(vectors):
    # State registers
    out_reg = 0
    prev_in = 0
    after_reset = False
    cur_reset = 0
    cur_in = 0
    result = []

    for row in vectors:
        # Drive row's inputs before the sampled posedge
        if "reset" in row:
            cur_reset = row["reset"]
        if "in" in row:
            cur_in = row["in"]

        in_val = cur_in & 0xFFFFFFFF
        reset_bit = cur_reset & 1

        # sync_active_high_reset: synchronous active-high reset clears sticky out and
        # marks the next non-reset cycle to ignore any transition from the reset cycle.
        if reset_bit == 1:
            out_reg = 0
            after_reset = True
            prev_in = in_val
        else:
            # capture_sticky_one_to_zero: reset clears/ignores previous input history,
            # so the first cycle after reset cannot capture a 1-to-0 transition.
            if after_reset:
                after_reset = False
                # out_reg remains 0 from reset
            else:
                not_in = (~in_val) & 0xFFFFFFFF
                capture = prev_in & not_in
                out_reg = (out_reg | capture) & 0xFFFFFFFF
            prev_in = in_val

        result.append({"out": out_reg})

        # Optional mid-row changes occur after sampling and before the next posedge.
        if "mid" in row:
            mid = row["mid"]
            if "reset" in mid:
                cur_reset = mid["reset"]
            if "in" in mid:
                cur_in = mid["in"]

    return result
