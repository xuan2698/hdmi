def reference(vectors):
    # Contract implementation for 2's complementer Moore FSM.
    # R3: async reset forces state S0 and z=0 (same cycle).
    # R1: state S0 -> z = x (registered, visible next cycle).
    # R2: state S1 -> z = ~x (registered, visible next cycle).
    # R4: posedge, areset==0: if S0 and x==1 -> S1; else unchanged.
    # Moore output: z is registered on posedge and visible next cycle.
    # Mid changes occur AFTER sampling, carried to next row.

    state = "S0"   # current state
    z_reg = 0      # registered output (Moore)

    results = []
    for row in vectors:
        areset = row.get("areset", 0)
        x = row.get("x", 0)

        # R3: asynchronous reset - same cycle effect
        if areset == 1:
            state = "S0"
            z_reg = 0
            results.append({"z": z_reg})
            # mid changes carried to next row (none here)
            continue

        # At posedge with areset==0:
        # Output is registered Moore value from previous state (visible this cycle).
        # Then compute next state and next registered output.
        # R1/R2: z depends on current state and current x, registered -> next cycle.
        if state == "S0":
            next_z = x & 1          # R1
        else:
            next_z = (~x) & 1       # R2

        # R4: next state transition
        if state == "S0" and x == 1:
            next_state = "S1"
        else:
            next_state = state

        # Output visible this cycle is the previously registered z_reg
        results.append({"z": z_reg})

        # Update registers for next cycle
        state = next_state
        z_reg = next_z

    return results
