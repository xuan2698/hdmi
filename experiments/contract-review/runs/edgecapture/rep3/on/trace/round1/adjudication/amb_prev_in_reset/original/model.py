def reference(vectors):
    out_reg = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    mask = 0xFFFFFFFF
    result = []

    for row in vectors:
        # Drive row values before the sampled posedge.
        cur_reset = row.get("reset", cur_reset)
        cur_in = row.get("in", cur_in) & mask

        # At posedge clk, sample reset and in and update the register state.
        if cur_reset == 1:
            # sync_reset_clear_out: reset == 1 at sampled posedge; out becomes 0.
            out_reg = 0
            # prev_in is still updated on every posedge, including reset cycles.
            prev_in = cur_in & mask
        else:
            # falling_edge_capture_and_hold: out_next = out OR (prev_in AND ~in)
            fall_mask = prev_in & ((~cur_in) & mask)
            out_reg = (out_reg | fall_mask) & mask
            prev_in = cur_in & mask

        # Outputs are visible in the same cycle after the sampled posedge.
        result.append({"out": out_reg & mask})

        # Optional mid changes occur after sampling, before the other edge.
        # They are carried to the start of the next row.
        mid = row.get("mid", None)
        if mid is not None:
            cur_reset = mid.get("reset", cur_reset)
            cur_in = mid.get("in", cur_in) & mask

    return result
