def reference(vectors):
    current_reset = 0
    current_in = 0
    out_reg = 0
    prev_in = 0
    result = []
    for row in vectors:
        if "reset" in row:
            current_reset = row["reset"]
        if "in" in row:
            current_in = row["in"]
        # sync_active_high_reset: reset clears out_reg, overrides capture.
        if current_reset:
            out_reg = 0
        else:
            # capture_sticky_one_to_zero: sticky capture of 1->0 transitions.
            transitions = prev_in & ((~current_in) & 0xFFFFFFFF)
            out_reg = (out_reg | transitions) & 0xFFFFFFFF
        # prev_in updates on every posedge, including reset cycles.
        prev_in = current_in & 0xFFFFFFFF
        result.append({"out": out_reg})
        # mid changes occur after sampling and carry to next row start.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                if "reset" in mid:
                    current_reset = mid["reset"]
                if "in" in mid:
                    current_in = mid["in"]
    return result
