def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # Compute next state and output based on current state and inputs
        if reset == 1:
            # R1: sync reset, active high -> start_shifting = 0, state = S0
            next_state = S0
            next_out = 0
        else:
            if state == S4:
                # R2/R5: hold start_shifting high forever until reset
                next_state = S4
                next_out = 1
            else:
                # Compute next state from current state and data
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
                    # R3: sequence found this cycle -> start_shifting = 1
                    next_out = 1
                else:
                    # R4: no match -> start_shifting = 0
                    next_out = 0

        # Output visible same cycle (posedge)
        out.append({'start_shifting': next_out})

        # Update state and output register for next cycle
        state = next_state
        start_shifting = next_out

    return out
