def reference(vectors):
    # State: out_reg (32-bit sticky flag), prev_in (32-bit previous input)
    # R1_reset_clear: reset==1 at posedge -> out_reg = 0
    # R2_capture_falling_edge: reset==0 and (prev_in & ~in) != 0 -> out_reg |= (prev_in & ~in)
    # R3_hold_until_reset: reset==0 and no falling edge -> out_reg unchanged
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0)
        in_val = row.get('in', 0)
        # Sample at posedge: compute next state based on current inputs and prev_in
        if reset == 1:
            # R1_reset_clear
            out_reg = 0
        else:
            # R2_capture_falling_edge / R3_hold_until_reset
            falling = prev_in & (~in_val & 0xFFFFFFFF)
            out_reg = (out_reg | falling) & 0xFFFFFFFF
        # Output visible same cycle (after posedge settles)
        results.append({'out': out_reg & 0xFFFFFFFF})
        # Update prev_in for next cycle (mid changes carried to next row start)
        prev_in = in_val & 0xFFFFFFFF
    return results
