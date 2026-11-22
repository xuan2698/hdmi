def reference(vectors):
    # State encoding: 0=S0, 1=S1, 2=S2
    state = 0
    cur_areset = 0
    cur_x = 0
    out = []

    for row in vectors:
        # Apply values driven before the sampled posedge. Carried mid changes are already in cur_*.
        try:
            row_items = row.items()
        except AttributeError:
            row_items = ()

        for k, v in row_items:
            if k == "mid":
                continue
            if k == "areset":
                cur_areset = v
            elif k == "x":
                cur_x = v

        areset = cur_areset
        x = cur_x
        z = 0

        if areset == 1:
            # async_reset_z0: areset=1 asynchronously forces state S0 and z=0.
            state = 0
            z = 0
        else:
            if state == 0:
                if x == 0:
                    # s0_x0
                    state = 0
                    z = 0
                else:
                    # s0_x1
                    state = 1
                    z = 1
            elif state == 1:
                if x == 0:
                    # s1_x0
                    state = 1
                    z = 1
                else:
                    # s1_x1
                    state = 2
                    z = 0
            else:
                if x == 0:
                    # s2_x0
                    state = 1
                    z = 1
                else:
                    # s2_x1
                    state = 2
                    z = 0

        out.append({"z": z & 1})

        # Process optional mid changes after sampling; carry inputs/state to the next row.
        if "mid" in row:
            m = row["mid"]
            if m is not None:
                try:
                    mid_items = m.items()
                    for k, v in mid_items:
                        if k == "areset":
                            cur_areset = v
                            if v == 1:
                                # async_reset_z0: mid-asserted reset also forces S0.
                                state = 0
                        elif k == "x":
                            cur_x = v
                except AttributeError:
                    for mm in m:
                        try:
                            items2 = mm.items()
                            for k, v in items2:
                                if k == "areset":
                                    cur_areset = v
                                    if v == 1:
                                        # async_reset_z0: mid-asserted reset also forces S0.
                                        state = 0
                                elif k == "x":
                                    cur_x = v
                        except AttributeError:
                            try:
                                k = mm[0]
                                v = mm[1]
                                if k == "areset":
                                    cur_areset = v
                                    if v == 1:
                                        # async_reset_z0: mid-asserted reset also forces S0.
                                        state = 0
                                elif k == "x":
                                    cur_x = v
                            except Exception:
                                pass

    return out
