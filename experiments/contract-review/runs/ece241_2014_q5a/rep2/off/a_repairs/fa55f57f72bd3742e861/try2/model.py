def reference(vectors):
    # State machine for 2's complementer (LSB first)
    # States: S0 (no 1 seen yet), S1 (1 seen, complementing)
    # R4: async reset active high -> state S0, z=0
    # R1: S0 -> z = x
    # R2: S1 -> z = NOT x
    # R3: posedge transitions: S0->S1 if x=1 else S0; S1->S1 always

    state = "S0"  # power-up state (unspecified, but reset will set it)
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R4: asynchronous reset - takes priority, same cycle
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z})
            continue

        # R1 / R2: combinational output based on current state
        if state == "S0":
            z = x  # R1
        else:  # S1
            z = 1 - x  # R2 (NOT x)

        results.append({"z": z})

        # R3: posedge state transition (visible next cycle)
        if state == "S0":
            if x == 1:
                state = "S1"
            # else stay S0
        # S1 -> S1 always

    return results
