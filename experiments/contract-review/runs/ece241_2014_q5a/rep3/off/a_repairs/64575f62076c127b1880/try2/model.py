def reference(vectors):
    # Contract implementation.
    # R3: areset == 1 asynchronously forces state to S0 and z to 0 (same cycle).
    # R1: state == S0: z = x (Moore, registered on posedge, visible next cycle).
    # R2: state == S1: z = ~x (Moore, registered on posedge, visible next cycle).
    # R4: posedge clk, areset == 0: if state == S0 and x == 1 then next state = S1; else state unchanged.
    # Mid changes occur AFTER sampling, before the other edge, carried to start of next row.

    S0 = 0
    S1 = 1

    state = S0
    z_reg = 0  # registered output

    results = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle)
        if areset == 1:
            state = S0
            z_reg = 0
            results.append({'z': z_reg})
            continue

        # At posedge with areset == 0:
        # R1/R2: Moore output based on current state and x, registered -> visible next cycle
        if state == S0:
            z_next = x & 1          # R1: z = x
        else:
            z_next = (~x) & 1       # R2: z = ~x

        # R4: next state transition
        if state == S0 and x == 1:
            next_state = S1
        else:
            next_state = state

        # Output visible next cycle (registered Moore)
        z_reg = z_next
        state = next_state

        results.append({'z': z_reg})

    return results
