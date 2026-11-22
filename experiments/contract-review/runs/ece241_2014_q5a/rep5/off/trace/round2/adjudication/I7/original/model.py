def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore machine.
    # States: S0 = no 1 seen yet (pass through), S1 = 1 seen (complement).
    # Reset is asynchronous, active high, forces state to S0.
    # Output z is combinational from current state and x:
    #   R1: in S0, z = x
    #   R2: in S1, z = NOT x
    # State updates on posedge:
    #   R3: S0 + x=1 -> S1 ; S0 + x=0 -> S0
    #   R4: S1 -> S1 regardless of x
    # R5: areset=1 forces S0 immediately (same cycle), z follows R1/R2.

    state = "S0"  # power-up unspecified but we pick S0; reset will force it anyway
    results = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R5: asynchronous reset forces state to S0 immediately (same cycle)
        if areset == 1:
            state = "S0"

        # Combinational output based on (possibly reset-updated) state
        if state == "S0":
            # R1: z = x
            z = x
        else:
            # R2: z = NOT x
            z = 1 - x

        results.append({"z": z & 1})

        # Posedge state update (only if not in reset this cycle)
        # R3 / R4
        if areset == 0:
            if state == "S0":
                if x == 1:
                    state = "S1"  # R3: first 1 seen
                else:
                    state = "S0"  # R3: stay
            else:
                state = "S1"  # R4: remain in S1

    return results
