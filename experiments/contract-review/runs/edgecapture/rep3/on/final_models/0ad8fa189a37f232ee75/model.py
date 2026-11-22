def reference(vectors):
    # State: out_reg (32-bit capture register), prev_in (previous sampled input).
    out_reg = 0
    prev_in = 0
    carry = {"reset": 0, "in": 0}
    result = []

    for row in vectors:
        # At the start of each row, carried mid changes provide pre-edge values,
        # then explicit row values are driven before the sampled posedge.
        cur = {"reset": carry.get("reset", 0), "in": carry.get("in", 0)}
        for key in row:
            if key == "mid":
                continue
            cur[key] = row[key]

        reset_val = cur.get("reset", 0) & 1
        in_val = cur.get("in", 0) & 0xFFFFFFFF

        # Rule sync_reset_clear_out: active-high synchronous reset has priority;
        # out becomes 0 on the sampled posedge.
        if reset_val:
            out_next = 0
        else:
            # Rule falling_edge_capture_and_hold: capture each bit where previous
            # sampled input was 1 and current input is 0; OR holds prior captures.
            falling = prev_in & ((~in_val) & 0xFFFFFFFF)
            out_next = (out_reg | falling) & 0xFFFFFFFF

        # Rule falling_edge_capture_and_hold: prev_in updates on every posedge,
        # including reset cycles, per the uncertain-contract chosen candidate.
        prev_in_next = in_val
        out_reg = out_next & 0xFFFFFFFF
        prev_in = prev_in_next & 0xFFFFFFFF

        result.append({"out": out_reg})

        # Optional mid changes occur after sampling, before the other edge,
        # and are carried into the next row's pre-edge input values.
        next_carry = {}
        for key in cur:
            next_carry[key] = cur[key]
        if "mid" in row:
            mid = row["mid"]
            if mid:
                for key in mid:
                    next_carry[key] = mid[key]
        carry = next_carry

    return result
