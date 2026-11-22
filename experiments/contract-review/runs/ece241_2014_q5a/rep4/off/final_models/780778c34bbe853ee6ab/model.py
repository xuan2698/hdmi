def reference(vectors):
    # Contract implementation for a 2's complementer Moore machine.
    # States: S0 (no 1 seen yet), S1 (a 1 has been seen).
    # R4: async reset forces state S0 and z=0.
    # R1: in S0, z = x (combinational, same cycle).
    # R2: in S1, z = NOT x (combinational, same cycle).
    # R3: posedge transition S0->S1 when x=1; S1 stays S1; S0 stays S0 when x=0.

    state = "S0"  # power-up state (unspecified, but reset will set it)
    out = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R4: asynchronous reset - state forced to S0, z=0 regardless of clock
        if areset == 1:
            state = "S0"
            z = 0
            out.append({"z": z})
            continue

        # R1 / R2: combinational output based on current state and x
        if state == "S0":
            z = x  # R1
        else:  # S1
            z = 1 - x  # R2 (NOT x)

        out.append({"z": z})

        # R3: posedge transition (sampled after this row's values are driven)
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stay S0
        # S1 stays S1

    return out
