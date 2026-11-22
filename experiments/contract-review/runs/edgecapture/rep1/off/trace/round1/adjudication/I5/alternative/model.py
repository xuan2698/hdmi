def reference(vectors):
    # State: out_reg (32-bit sticky flag), prev_in (32-bit previous input)
    # R1_reset_clear: reset==1 at posedge -> out_reg = 0 (sync reset)
    # R2_capture_falling_edge: reset==0 and (prev_in & ~in) -> out_reg |= (prev_in & ~in)
    # R3_hold_until_reset: otherwise out_reg holds
    # Candidate interpretation (global): reset does not affect out until next posedge;
    #   out holds previous value during reset cycle. So we sample reset at posedge and
    #   apply reset effect at that posedge (visible same cycle per R1). The candidate
    #   interpretation says out holds during the reset cycle — meaning the reset's
    #   effect is applied at the posedge, and the output reported for that row reflects
    #   the state AFTER the posedge update. We follow R1 (visible same_cycle) since it
    #   is the primary rule; the candidate interpretation is about the cycle where
    #   reset is asserted — out holds previous value during that cycle, i.e., the
    #   update happens at the posedge (which is the sampling edge). We'll apply reset
    #   at the posedge (same cycle visible), consistent with R1.

    out_reg = 0
    prev_in = 0
    results = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        cur_in = row.get('in', 0) & 0xFFFFFFFF

        # posedge sampling: compute next state
        if reset == 1:
            # R1_reset_clear: synchronous reset clears out
            out_reg = 0
        else:
            # R2_capture_falling_edge: detect 1->0 transitions
            falling = prev_in & (~cur_in & 0xFFFFFFFF)
            if falling != 0:
                out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold_until_reset: else hold (no change)

        # prev_in updates to current input after sampling
        prev_in = cur_in

        results.append({'out': out_reg & 0xFFFFFFFF})

    return results
