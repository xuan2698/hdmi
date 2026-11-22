def reference(vectors):
    # R_RESET: synchronous active-high reset clears out at posedge, priority above fall.
    # R_FALL: detect prev_in[i] == 1 and in[i] == 0, set sticky out bits.
    # R_HOLD: bits not falling retain their previous value.
    # prev_in updates on every posedge, including reset edges.
    mask = 4294967295
    out = 0
    prev_in = 0
    cur_in = 0
    cur_reset = 0
    result = []

    def apply_changes(reset_val, in_val, changes):
        known = 0
        try:
            v = changes["in"]
            in_val = v & mask
            known = 1
        except:
            pass
        try:
            v = changes["reset"]
            reset_val = v & 1
            known = 1
        except:
            pass
        if known == 0:
            try:
                for sub in changes:
                    reset_val, in_val = apply_changes(reset_val, in_val, sub)
            except:
                pass
        return reset_val, in_val

    for row in vectors:
        # Inputs are driven before the sampled posedge. Missing keys retain carried values.
        try:
            cur_reset = row["reset"] & 1
        except:
            pass
        try:
            cur_in = row["in"] & mask
        except:
            pass

        # Sampled posedge update.
        if cur_reset:
            # R_RESET
            out = 0
            prev_in = cur_in & mask
        else:
            # R_FALL
            fall = prev_in & ((~cur_in) & mask)
            out = (out | fall) & mask
            # R_HOLD: non-falling bits stay unchanged.
            prev_in = cur_in & mask

        result.append({"out": out & mask})

        # Optional mid changes occur after sampling and carry to the next row.
        try:
            mid = row["mid"]
            cur_reset, cur_in = apply_changes(cur_reset, cur_in, mid)
        except:
            pass
        try:
            mid = row["mid_changes"]
            cur_reset, cur_in = apply_changes(cur_reset, cur_in, mid)
        except:
            pass
        try:
            cur_in = row["mid_in"] & mask
        except:
            pass
        try:
            cur_reset = row["mid_reset"] & 1
        except:
            pass

    return result
