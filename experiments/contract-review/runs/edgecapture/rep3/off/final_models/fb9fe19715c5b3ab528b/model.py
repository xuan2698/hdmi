def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit), prev_in (32-bit, previous sampled input).
    # Timing: sample at posedge clk; mid changes applied after sampling,
    # carried to start of next row.
    # Power-up: out_reg = 0, prev_in = 0 (concrete, unsigned).

    out_reg = 0
    prev_in = 0
    results = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        cur_in = row.get('in', 0) & 0xFFFFFFFF

        # R1_reset_clear: sync active-high reset clears out_reg at posedge.
        # R2_capture_falling: out <= out | (prev_in & ~in) when reset==0.
        # R3_hold: out <= out when no falling edge and reset==0.
        if reset == 1:
            # R1_reset_clear
            out_reg = 0
        else:
            # R2_capture_falling / R3_hold
            falling = prev_in & (~cur_in & 0xFFFFFFFF)
            out_reg = (out_reg | falling) & 0xFFFFFFFF

        # Output visible same cycle as the posedge (registered value after update).
        results.append({'out': out_reg & 0xFFFFFFFF})

        # Update prev_in to current sampled input for next cycle.
        prev_in = cur_in

        # Mid changes: applied AFTER sampling, carried to next row.
        # They affect prev_in for the next row's falling-edge detection.
        mid = row.get('mid')
        if mid is not None:
            if 'in' in mid:
                prev_in = mid['in'] & 0xFFFFFFFF
            # mid reset changes are not part of the contract's mid spec;
            # only input changes are carried.

    return results
