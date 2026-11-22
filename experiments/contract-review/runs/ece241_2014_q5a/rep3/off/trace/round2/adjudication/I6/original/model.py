def reference(vectors):
    # Contract implementation for a serial 2's complementer Moore FSM.
    #
    # State encoding:
    #   S0 = no 1-bit seen yet (copy phase): z = x
    #   S1 = a 1-bit has been seen (invert phase): z = ~x
    #
    # Reset (areset) is asynchronous, active high: forces state to S0 and z to 0.
    # Outputs are Moore-style: registered on posedge clk, visible next cycle.
    # Mid input changes occur AFTER sampling, before the other edge, and are
    # carried to the start of the next row.

    S0 = 0
    S1 = 1

    state = S0
    z = 0  # power-up value; unspecified but concrete

    results = []

    for row in vectors:
        areset = row.get("areset", 0) & 1
        x = row.get("x", 0) & 1

        # R3: asynchronous reset forces state to S0 and z to 0 (same cycle).
        if areset == 1:
            state = S0
            z = 0
            results.append({"z": z & 1})
            continue

        # R1 / R2: Moore output based on current state (visible this cycle,
        # i.e., registered from the previous posedge).
        if state == S0:
            # R1: state == S0 -> z = x
            z = x & 1
        else:
            # R2: state == S1 -> z = ~x
            z = (~x) & 1

        # R4: posedge clk transition (next state).
        # If state == S0 and x == 1 -> next state = S1; else unchanged.
        if state == S0 and x == 1:
            next_state = S1
        else:
            next_state = state

        results.append({"z": z & 1})

        # Mid changes are carried to the start of the next row; state update
        # happens at the posedge, so apply it now for the next iteration.
        state = next_state

    return results
