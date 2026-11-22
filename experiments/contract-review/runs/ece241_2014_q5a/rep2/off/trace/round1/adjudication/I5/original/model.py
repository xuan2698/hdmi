def reference(vectors):
    # State machine: S0 = no 1 seen yet (pass through), S1 = complementing
    # R4: async reset -> S0, z=0
    # R1: S0 -> z = x
    # R2: S1 -> z = NOT x
    # R3: posedge: S0->S1 if x=1, S0->S0 if x=0, S1->S1 always
    state = "S0"
    out = []
    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)
        # R4: asynchronous reset dominates, visible same cycle
        if areset == 1:
            state = "S0"
            z = 0
        else:
            # R1 / R2: combinational output based on current state
            if state == "S0":
                z = x & 1  # R1
            else:
                z = (~x) & 1  # R2
        out.append({"z": z})
        # R3: posedge state transition (only when not in reset)
        if areset == 0:
            if state == "S0":
                if x == 1:
                    state = "S1"
                else:
                    state = "S0"
            else:
                state = "S1"
        # mid changes are carried to next row; nothing to do here
    return out
