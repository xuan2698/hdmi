def reference(vectors):
    # R1_reset_clear: synchronous active-high reset clears out_reg
    # R2_capture_falling_edge: set sticky bits where prev_in & ~in
    # R3_hold_until_reset: otherwise hold out_reg
    # R4_prev_in_tracks_all_cycles: prev_in updates only when reset==0
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row["reset"] & 1
        in_val = row["in"] & 0xFFFFFFFF
        # posedge sampling
        if reset == 1:
            # R1_reset_clear
            out_reg = 0
            # R4: prev_in holds during reset (not updated)
        else:
            # R2_capture_falling_edge
            falling = prev_in & (~in_val & 0xFFFFFFFF)
            out_reg = out_reg | falling
            # R3_hold_until_reset is implicit: out_reg retains prior bits
            # R4_prev_in_tracks_all_cycles
            prev_in = in_val
        results.append({"out": out_reg & 0xFFFFFFFF})
    return results
