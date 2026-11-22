def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    # States: S0 (no 1 seen yet), S1 (at least one 1 seen).
    # R4: async reset (areset=1) forces state to S0 and z=0, same cycle.
    # R1: in S0, z = x (combinational, same cycle).
    # R2: in S1, z = NOT x (combinational, same cycle).
    # R3: posedge transition: S0->S1 if x=1 else S0; S1->S1 always.
    #     Same-cycle z uses current state; transition visible next cycle.
    # Mid changes occur after sampling, carried to next row.

    state = "S0"  # power-up state
    results = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R4: asynchronous reset asserted -> state S0, z forced 0 (same cycle)
        if areset == 1:
            state = "S0"
            z = 0
            results.append({"z": z & 1})
            # Reset asserted: no posedge state update (update_during_reset false)
            continue

        # Combinational output based on current state (R1 / R2)
        if state == "S0":
            # R1: z = x
            z = x
        else:
            # R2: z = NOT x
            z = 1 - x

        results.append({"z": z & 1})

        # R3: posedge state transition (effective next cycle)
        if state == "S0":
            if x == 1:
                state = "S1"
            else:
                state = "S0"
        else:
            state = "S1"

    return results
