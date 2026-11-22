def reference(vectors):
    # State encoding: 0 = A (reset), 1 = B, 2 = C
    state = 0
    cur_areset = 0
    cur_x = 0
    out = []

    for row in vectors:
        # Row inputs are driven before the sampled posedge.
        if "areset" in row:
            cur_areset = row["areset"]
        if "x" in row:
            cur_x = row["x"]

        # async_reset: active-high areset asynchronously forces state A and z=0.
        if cur_areset:
            state = 0

        # serial_twos_complement: posedge transition when reset is released.
        if not cur_areset:
            if state == 0:
                if cur_x:
                    state = 1
            elif state == 1:
                if cur_x:
                    state = 2
            else:  # state == 2
                if cur_x:
                    state = 2
                else:
                    state = 1

        # Moore output after settled posedge: B -> 1, A/C -> 0.
        if state == 1:
            z = 1
        else:
            z = 0
        out.append({"z": z})

        # mid changes occur after sampling and are carried to the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                try:
                    items = mid.items()
                    for k, v in items:
                        if k == "areset":
                            cur_areset = v
                            # async_reset: mid-cycle assertion resets state immediately.
                            if cur_areset:
                                state = 0
                        elif k == "x":
                            cur_x = v
                except:
                    for change in mid:
                        if "areset" in change:
                            cur_areset = change["areset"]
                            if cur_areset:
                                state = 0
                        if "x" in change:
                            cur_x = change["x"]

        # Support direct mid_* keys if present.
        if "mid_areset" in row:
            cur_areset = row["mid_areset"]
            if cur_areset:
                state = 0
        if "mid_x" in row:
            cur_x = row["mid_x"]

    return out
