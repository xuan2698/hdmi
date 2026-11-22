def reference(vectors):
    # State: out_reg holds sticky flags, prev_in holds previous input value.
    # R1_reset_clear: synchronous active-high reset clears out_reg (visible same cycle).
    # R2_capture_falling_edge: on posedge with reset==0, set bits where prev_in=1 and in=0.
    # R3_hold_until_reset: bits already set remain set until reset.
    # Mid changes occur AFTER sampling; carried to start of next row.

    out_reg = 0
    prev_in = 0
    results = []

    for row in vectors:
        reset = row.get("reset", 0) & 1
        cur_in = row.get("in", 0) & 0xFFFFFFFF

        # Sampling at posedge clk: compute next state from current inputs and prev_in.
        if reset == 1:
            # R1_reset_clear
            next_out = 0
        else:
            # R2_capture_falling_edge: detect 1->0 transitions
            falling = prev_in & (~cur_in) & 0xFFFFFFFF
            # R3_hold_until_reset: keep existing flags, add new falling edges
            next_out = (out_reg | falling) & 0xFFFFFFFF

        # Output visible for this cycle is the registered value after the edge.
        out_reg = next_out
        results.append({"out": out_reg & 0xFFFFFFFF})

        # Mid changes: input may change AFTER sampling; carry to next row's prev_in.
        # The "in" value used for next cycle's prev_in is the post-mid value.
        # Since mid changes are optional and not explicitly given, we use cur_in
        # as the value carried forward (the sampled value persists unless mid changes).
        prev_in = cur_in

    return results
