def reference(vectors):
    # Contract implementation.
    # State: out_reg (32-bit sticky flag), in_prev (32-bit previous input).
    # Initial: out_reg = 0, in_prev = 0 (R2 candidate: in_prev=0 before first cycle).
    out_reg = 0
    in_prev = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        inp = row.get('in', 0) & 0xFFFFFFFF
        # R1_reset_clear: reset==1 -> out cleared (priority 1)
        if reset == 1:
            out_reg = 0
        else:
            # R2_capture_falling: bits that were 1 in in_prev and 0 now
            falling = in_prev & (~inp) & 0xFFFFFFFF
            # R3_hold: keep existing bits, OR in new captures
            out_reg = (out_reg | falling) & 0xFFFFFFFF
        # Output visible this cycle (same_cycle for reset, next_cycle for capture
        # is handled by the fact that we sample in_prev from prior row).
        results.append({'out': out_reg & 0xFFFFFFFF})
        # Update in_prev for next cycle (mid changes carried to start of next row)
        in_prev = inp
    return results
