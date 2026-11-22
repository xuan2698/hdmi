def reference(vectors):
    # State: out_reg (sticky per-bit flag), prev_in (last sampled input)
    # R4_prev_in_tracks_all_cycles: prev_in updates every posedge including reset cycles
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row["reset"] & 1
        inp = row["in"] & 0xFFFFFFFF
        # R1_reset_clear: synchronous reset clears out_reg (priority 1)
        if reset == 1:
            out_reg = 0
        else:
            # R2_capture_falling_edge: capture 1->0 transitions using prev_in
            falling = prev_in & (~inp & 0xFFFFFFFF)
            out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold_until_reset: out_reg retains previous value otherwise
        # R4_prev_in_tracks_all_cycles: prev_in updated every posedge including reset
        prev_in = inp
        results.append({"out": out_reg & 0xFFFFFFFF})
    return results
