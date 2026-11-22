def reference(vectors):
    # State: out (32-bit sticky falling-edge flags), prev_in (32-bit previous input)
    # R1_reset_clear: sync active-high reset clears out to 0 on posedge
    # R2_capture_falling: on posedge with reset==0, out |= prev_in & ~in
    # R3_hold: out retains value when no falling edges
    out = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        cur_in = row.get('in', 0) & 0xFFFFFFFF
        # R1_reset_clear: synchronous reset takes priority
        if reset == 1:
            out = 0
        else:
            # R2_capture_falling: capture 1->0 transitions
            out = out | (prev_in & (~cur_in & 0xFFFFFFFF))
            # R3_hold: out unchanged otherwise (implicit)
        # Update prev_in for next cycle (mid changes carried to next row start)
        prev_in = cur_in
        results.append({'out': out & 0xFFFFFFFF})
    return results
