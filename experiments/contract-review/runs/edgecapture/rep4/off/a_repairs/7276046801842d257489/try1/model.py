def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit sticky flag), in_prev (previous sampled input).
    # R1_reset_clear: sync active-high reset clears out_reg at posedge (priority 1).
    # R2_capture_falling: on posedge with reset==0, set bits where in_prev=1 and in=0 (priority 2).
    # R3_hold: out_reg retains value otherwise (priority 3).
    # Mid changes occur AFTER sampling, before next edge; carried to next row.
    # Power-up: out_reg=0, in_prev=0 (unspecified but concrete).

    out_reg = 0
    in_prev = 0
    results = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        cur_in = row.get('in', 0) & 0xFFFFFFFF

        # Sampling at posedge: compute next state based on current inputs and prior state.
        if reset == 1:
            # R1_reset_clear
            next_out = 0
        else:
            # R2_capture_falling: bits that were 1 previously and are 0 now
            falling = in_prev & (~cur_in) & 0xFFFFFFFF
            # R3_hold: keep existing flags, OR in new falling captures
            next_out = (out_reg | falling) & 0xFFFFFFFF

        # Output visible same cycle for reset (R1), next cycle for capture/hold.
        # Per contract examples, output reflects the register value AFTER the edge.
        out_reg = next_out
        in_prev = cur_in

        results.append({'out': out_reg & 0xFFFFFFFF})

    return results
