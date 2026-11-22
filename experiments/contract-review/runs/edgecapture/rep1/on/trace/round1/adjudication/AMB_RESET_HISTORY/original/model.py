def reference(vectors):
    # Named state: out is the sticky capture register.
    out = 0
    # Named state: prev_in is the previous sampled input vector.
    prev_in = 0
    # Current wire values, possibly carried from prior mid changes.
    cur_reset = 0
    cur_in = 0
    result = []

    for row in vectors:
        # Drive this row's values before the sampled posedge.
        if 'reset' in row:
            cur_reset = row['reset'] & 1
        if 'in' in row:
            cur_in = row['in'] & 0xFFFFFFFF

        sample_reset = cur_reset
        sample_in = cur_in

        # R_RESET: active-high synchronous reset has priority and clears out.
        if sample_reset == 1:
            out = 0
        else:
            # R_FALL: detect 1-to-0 transitions using prev_in and sample_in.
            # R_HOLD: bits without a falling edge retain their previous value.
            falling = prev_in & (~sample_in & 0xFFFFFFFF)
            out = (out | falling) & 0xFFFFFFFF

        # prev_in updates on every posedge, including reset.
        # out is visible in the same sampled cycle.
        prev_in = sample_in & 0xFFFFFFFF
        result.append({'out': out & 0xFFFFFFFF})

        # Mid input changes occur after sampling and are carried to next row.
        if 'mid' in row:
            mid = row['mid']
            if mid:
                if 'reset' in mid:
                    cur_reset = mid['reset'] & 1
                if 'in' in mid:
                    cur_in = mid['in'] & 0xFFFFFFFF

    return result
