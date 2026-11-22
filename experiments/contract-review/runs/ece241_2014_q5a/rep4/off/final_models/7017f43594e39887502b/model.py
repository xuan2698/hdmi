def reference(vectors):
    # Contract implementation.
    # State: S0 = no 1-bit seen yet (trailing zeros), S1 = complementing.
    # Outputs are combinational from current state and current x (R1, R2),
    # except async reset forces z=0 (R4).
    # State updates on posedge using x sampled at that edge (R3).
    # Mid-cycle changes after the edge affect only the next row (R3, mid).

    state = "S0"  # power-up state
    out = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R4: asynchronous reset forces state S0 and z=0 regardless of clock.
        if areset:
            state = "S0"
            z = 0
            out.append({"z": z})
            continue

        # R1: In S0, z = x (trailing zeros pass through; first 1 outputs 1).
        # R2: In S1, z = NOT x.
        if state == "S0":
            z = x  # R1
        else:
            z = 1 - x  # R2

        out.append({"z": z})

        # R3: posedge state transition using x sampled at the edge.
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stay S0
        else:
            state = "S1"  # S1 stays S1

    return out
