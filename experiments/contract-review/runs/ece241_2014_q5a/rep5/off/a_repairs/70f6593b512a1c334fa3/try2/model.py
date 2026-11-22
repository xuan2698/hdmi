def reference(vectors):
    # Contract implementation for 2's complementer Moore FSM.
    # State: S0 (no 1 seen yet), S1 (at least one 1 seen).
    # R5: async reset (areset=1) forces state S0 and z=0 immediately.
    # R1: In S0, z = x (combinational, same cycle).
    # R2: In S1, z = NOT x (combinational, same cycle).
    # R3: On posedge, if x=1 then next state S1; if x=0 stay S0.
    # R4: On posedge, once in S1, stay S1 regardless of x.
    # Mid changes occur after sampling, carried to start of next row.

    state = "S0"
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R5: asynchronous reset forces state S0 and z=0 immediately.
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z})
            # Reset is async; mid changes carried to next row start.
            # State remains S0 after reset.
            continue

        # Combinational output based on current state (R1 / R2).
        if state == "S0":
            z = x  # R1
        else:
            z = 1 - x  # R2

        results.append({"z": z})

        # Posedge state update (R3 / R4) — sampling happens at edge.
        if state == "S0":
            if x == 1:
                state = "S1"  # R3
            # else stay S0
        else:
            state = "S1"  # R4

    return results
