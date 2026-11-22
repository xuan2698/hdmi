def reference(vectors):
    # State: out_reg (32-bit sticky flag), prev_in (32-bit previous input)
    # R1_reset_clear: reset==1 at posedge -> out cleared to 0 (priority 1)
    # R2_capture_falling_edge: reset==0 and (prev_in & ~in)!=0 -> set bits (priority 2)
    # R3_hold_until_reset: reset==0 and no falling edge -> hold (priority 3)
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        in_val = row.get('in', 0) & 0xFFFFFFFF
        # Sample at posedge: compute next state from current inputs and prev_in
        if reset == 1:
            # R1_reset_clear
            out_reg = 0
        else:
            # R2_capture_falling_edge
            falling = prev_in & (~in_val) & 0xFFFFFFFF
            if falling != 0:
                out_reg = (out_reg | falling) & 0xFFFFFFFF
            # R3_hold_until_reset: out_reg unchanged
        # Update prev_in for next cycle (input sampled at this edge)
        prev_in = in_val
        results.append({'out': out_reg & 0xFFFFFFFF})
    return results
