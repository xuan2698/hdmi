def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit sticky flag), in_prev (previous sampled input).
    # R1_reset_clear: sync active-high reset clears out_reg at posedge.
    # R2_capture_falling: at posedge, for each bit, if in_prev bit==1 and in bit==0, set out_reg bit.
    # R3_hold: out_reg bits otherwise retain their value.
    # Mid changes occur after sampling and are carried to next row's input.

    out_reg = 0
    in_prev = 0
    results = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        cur_in = row.get('in', 0) & 0xFFFFFFFF

        # R1_reset_clear: synchronous reset has priority
        if reset == 1:
            out_reg = 0
        else:
            # R2_capture_falling: detect 1->0 transitions on each bit
            falling = in_prev & (~cur_in) & 0xFFFFFFFF
            out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold: bits not newly falling retain value (implicit)

        # Sample output after posedge settled
        results.append({'out': out_reg & 0xFFFFFFFF})

        # Update previous input for next cycle (mid changes carried forward)
        in_prev = cur_in

    return results
