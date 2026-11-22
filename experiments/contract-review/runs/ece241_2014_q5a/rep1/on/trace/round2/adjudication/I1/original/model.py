def reference(vectors):
    # State encoding:
    # 0 = A (Reset, z=0)
    # 1 = B (one seen, z=0)
    # 2 = C (one seen, z=1)
    state = 0
    areset = 0
    x = 0
    outputs = []

    for row in vectors:
        # Drive row inputs before the sampled posedge.
        if "areset" in row:
            areset = row["areset"]
        if "x" in row:
            x = row["x"]

        # Sample after the posedge has settled.
        if areset == 1:
            # reset_async_z0: asynchronous reset forces A and z=0.
            state = 0
            z = 0
        else:
            if state == 0:  # A
                if x == 0:
                    # A_x0_to_A_z0
                    state = 0
                    z = 0
                else:
                    # A_x1_to_C_z1
                    state = 2
                    z = 1
            elif state == 1:  # B
                if x == 0:
                    # B_x0_to_C_z1
                    state = 2
                    z = 1
                else:
                    # B_x1_to_B_z0
                    state = 1
                    z = 0
            else:  # C
                if x == 0:
                    # C_x0_to_C_z1
                    state = 2
                    z = 1
                else:
                    # C_x1_to_B_z0
                    state = 1
                    z = 0

        outputs.append({"z": z})

        # Optional mid changes happen AFTER sampling and before the other edge.
        # They persist into the start of the next row.
        if "mid" in row:
            mid = row["mid"]
            if mid:
                try:
                    # Treat mid as a mapping of input name -> value.
                    for k in mid:
                        v = mid[k]
                        if k == "areset":
                            areset = v
                            if areset == 1:
                                state = 0  # asynchronous reset applies immediately
                        elif k == "x":
                            x = v
                except:
                    # Otherwise treat mid as a sequence of mapping entries.
                    for entry in mid:
                        for k in entry:
                            v = entry[k]
                            if k == "areset":
                                areset = v
                                if areset == 1:
                                    state = 0
                            elif k == "x":
                                x = v

    return outputs
