def reference(vectors):
    # async_reset: initial state A (reset state)
    state = 0  # 0=A, 1=B, 2=C
    cur_areset = 0
    cur_x = 0
    out = []
    for row in vectors:
        # Apply inputs driven before the sampled edge
        if "areset" in row:
            cur_areset = row["areset"]
        if "x" in row:
            cur_x = row["x"]

        # async_reset: asserted high asynchronously forces state A and z=0
        if cur_areset == 1:
            state = 0

        # serial_twos_complement: z reflects pre-edge Moore state (lag interpretation)
        if state == 0:
            z = 0
        elif state == 1:
            z = 1
        else:
            z = 0
        out.append({"z": z})

        # serial_twos_complement: posedge update, reset has priority
        if cur_areset == 1:
            state = 0
        else:
            if state == 0:       # A
                if cur_x == 0:
                    state = 0
                else:
                    state = 1
            elif state == 1:     # B
                if cur_x == 0:
                    state = 1
                else:
                    state = 2
            else:                # C
                if cur_x == 0:
                    state = 1
                else:
                    state = 2

        # mid changes occur after the sampled posedge
        if "mid" in row:
            mid = row["mid"]
            if mid:
                if "areset" in mid:
                    cur_areset = mid["areset"]
                    # async_reset: mid assertion asynchronously forces state A
                    if cur_areset == 1:
                        state = 0
                if "x" in mid:
                    cur_x = mid["x"]
    return out
