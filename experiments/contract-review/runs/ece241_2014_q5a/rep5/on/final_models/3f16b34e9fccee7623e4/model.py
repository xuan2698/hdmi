def reference(vectors):
    # async_reset_assert: active-high areset forces state A and z=0 when asserted before the sampled edge.
    # A_on_x0: A with x=0 stays A, z=0.
    # A_on_x1: A with x=1 goes B, z=1.
    # B_on_x0: B with x=0 stays B, z=1.
    # B_on_x1: B with x=1 goes C, z=0.
    # C_on_x0: C with x=0 goes B, z=1.
    # C_on_x1: C with x=1 stays C, z=0.
    state = "A"
    cur_areset = 0
    cur_x = 0
    result = []

    for row in vectors:
        if "areset" in row:
            cur_areset = row["areset"]
        if "x" in row:
            cur_x = row["x"]

        if cur_areset == 1:
            # async_reset_assert
            state = "A"
            z = 0
        else:
            if state == "A":
                if cur_x == 0:
                    # A_on_x0
                    state = "A"
                    z = 0
                else:
                    # A_on_x1
                    state = "B"
                    z = 1
            elif state == "B":
                if cur_x == 0:
                    # B_on_x0
                    state = "B"
                    z = 1
                else:
                    # B_on_x1
                    state = "C"
                    z = 0
            else:
                if cur_x == 0:
                    # C_on_x0
                    state = "B"
                    z = 1
                else:
                    # C_on_x1
                    state = "C"
                    z = 0

        result.append({"z": z})

        if "mid" in row:
            mid = row["mid"]
            if "areset" in mid:
                cur_areset = mid["areset"]
                if cur_areset == 1:
                    # async_reset_assert
                    state = "A"
            if "x" in mid:
                cur_x = mid["x"]

    return result
