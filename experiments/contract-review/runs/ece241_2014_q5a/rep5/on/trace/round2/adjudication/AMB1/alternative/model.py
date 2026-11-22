def reference(vectors):
    # global: apply active-low reset override; areset=0 asserts reset, areset=1 releases.
    state = "A"
    areset = 0
    x = 0
    out = []

    for row in vectors:
        # Row values are driven before the sampled posedge, carrying prior mid changes.
        if "areset" in row:
            areset = row["areset"]
        if "x" in row:
            x = row["x"]

        # async_reset_assert: active-low reset forces state A and visible z=0.
        if areset == 0:
            state = "A"
            z = 0
        else:
            # Positive-edge transition when reset is released.
            if state == "A":
                if x == 0:
                    # A_on_x0: A remains A, z=0
                    state = "A"
                else:
                    # A_on_x1: A becomes B, z=1
                    state = "B"
            elif state == "B":
                if x == 0:
                    # B_on_x0: B remains B, z=1
                    state = "B"
                else:
                    # B_on_x1: B becomes C, z=0
                    state = "C"
            else:
                if x == 0:
                    # C_on_x0: C becomes B, z=1
                    state = "B"
                else:
                    # C_on_x1: C remains C, z=0
                    state = "C"

            if state == "A":
                z = 0
            elif state == "B":
                z = 1
            else:
                z = 0

        out.append({"z": z})

        # Optional mid changes occur after sampling and are carried to the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid is not None:
                if "areset" in mid:
                    areset = mid["areset"]
                    # async_reset_assert: mid reset assertion asynchronously forces state A.
                    if areset == 0:
                        state = "A"
                if "x" in mid:
                    x = mid["x"]

    return out
