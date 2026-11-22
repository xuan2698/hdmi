def reference(vectors):
    # Contract implementation for serial 2's complementer Moore FSM.
    # States: S0 (no 1 seen yet), S1 (at least one 1 seen).
    # R4: async reset (areset=1) -> state S0, z=0, same cycle.
    # R1: in S0, z = x (combinational, same cycle).
    # R2: in S1, z = NOT x (combinational, same cycle).
    # R3: posedge transition: S0->S1 if x=1 else S0; S1->S1 always.
    #     Same-cycle z uses current state (before transition).
    # Mid changes occur after sampling, carried to next row.

    state = "S0"  # power-up state
    out = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R4: asynchronous reset dominates, same cycle
        if areset:
            state = "S0"
            z = 0
        else:
            # R1 / R2: combinational output based on current state
            if state == "S0":
                z = x  # R1
            else:
                z = 1 - x  # R2 (NOT x)

        out.append({"z": z & 1})

        # R3: posedge state transition (effective next cycle)
        # Only when not in reset (update_during_reset false)
        if not areset:
            if state == "S0":
                if x == 1:
                    state = "S1"
                # else stay S0
            else:
                state = "S1"  # S1 -> S1 always

    return out
