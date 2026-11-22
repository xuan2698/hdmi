def reference(vectors):
    # Contract implementation.
    # State: S0 = no 1-bit seen yet (copy phase), S1 = 1-bit seen (invert phase).
    # R3: areset high asynchronously forces state to S0 and z to 0 (same cycle).
    # R1: state == S0 -> z = x (registered, visible next cycle).
    # R2: state == S1 -> z = ~x (registered, visible next cycle).
    # R4: posedge clk, areset == 0: if state == S0 and x == 1 then next state = S1;
    #     else state unchanged (S1 remains S1 until reset).
    # Moore output: z is registered on posedge clk, visible next cycle.
    # Mid input changes occur AFTER sampling, before the other edge, carried to next row.

    state = "S0"   # power-up state
    z_reg = 0      # registered output

    results = []
    for row in vectors:
        areset = row["areset"]
        x = row["x"]

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle, visible now)
        if areset == 1:
            state = "S0"
            z_reg = 0
            results.append({"z": z_reg})
            # mid changes after sampling: none affect state here since reset holds
            continue

        # areset == 0: posedge clk sampling
        # Compute next state per R4
        if state == "S0" and x == 1:
            next_state = "S1"
        else:
            next_state = state

        # Compute next registered output per R1/R2 based on current state and x
        if state == "S0":
            next_z = x & 1          # R1: z = x
        else:
            next_z = (~x) & 1       # R2: z = ~x

        # Apply posedge update (visible next cycle)
        state = next_state
        z_reg = next_z

        results.append({"z": z_reg})

    return results
