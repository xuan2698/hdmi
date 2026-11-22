def reference(vectors):
    # State encoding: S0=0, S1=1, S2=2, S3=3, S4=4
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    state = S0
    start_shifting = 0
    out = []

    for vec in vectors:
        reset = vec["reset"]
        data = vec["data"]

        # Compute next state and output based on current state and inputs (posedge sampling)
        if reset == 1:
            # R1: synchronous active-high reset -> start_shifting=0, state=S0
            next_state = S0
            next_out = 0
        else:
            if state == S4:
                # R2 / R5: latched forever until reset
                next_state = S4
                next_out = 1
            else:
                # Determine next state from current state and data
                if state == S0:
                    next_state = S1 if data == 1 else S0
                elif state == S1:
                    next_state = S2 if data == 1 else S0
                elif state == S2:
                    next_state = S3 if data == 0 else S2
                elif state == S3:
                    next_state = S4 if data == 1 else S0
                else:
                    next_state = S4

                if next_state == S4:
                    # R3: transition into S4 sets start_shifting=1 same cycle
                    next_out = 1
                else:
                    # R4: no match, start_shifting stays 0
                    next_out = 0

        # Output visible same cycle as the posedge (based on next state / reset)
        out.append({"start_shifting": next_out})

        # Update state for next cycle
        state = next_state
        start_shifting = next_out

    return out
