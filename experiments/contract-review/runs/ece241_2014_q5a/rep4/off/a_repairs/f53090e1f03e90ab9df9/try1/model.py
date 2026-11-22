def reference(vectors):
    # Contract implementation for 2's complement Moore machine.
    # R4: async reset (areset=1) forces state S0 and z=0 regardless of clock.
    # R1: In state S0, z = x (combinational, same cycle).
    # R2: In state S1, z = NOT x (combinational, same cycle).
    # R3: posedge transition: S0->S1 when x=1; S1 stays S1; S0 stays S0 when x=0.
    # Mid changes occur after sampling edge, carried to start of next row.

    state = "S0"  # power-up state
    results = []

    for vec in vectors:
        areset = vec.get("areset", 0)
        x = vec.get("x", 0)

        # R4: asynchronous reset dominates - state forced to S0, z=0
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z})
            # mid changes carried to next row (state already S0)
            continue

        # Combinational output based on current state (R1 / R2)
        if state == "S0":
            z = x  # R1
        else:  # S1
            z = 1 - x  # R2

        results.append({"z": z})

        # R3: posedge state transition (sampled at this edge)
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stays S0
        # S1 stays S1

    return results
