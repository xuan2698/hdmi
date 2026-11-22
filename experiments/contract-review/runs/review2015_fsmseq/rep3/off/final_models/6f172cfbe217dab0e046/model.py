def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Power-up state (unspecified, choose S0) and output latch
    state = S0
    start_shifting = 0

    results = []
    for row in vectors:
        reset = row["reset"] & 1
        data = row["data"] & 1

        # --- Compute next state and next output (sampled at posedge) ---
        # R1: reset == 1 -> start_shifting = 0 (priority 1)
        if reset == 1:
            next_state = S0
            next_out = 0
        else:
            # R2: state == S4 -> start_shifting stays 1 (priority 2)
            if state == S4:
                next_state = S4
                next_out = 1
            # R3: state == S3 and data == 1 -> sequence found, latch high (priority 3)
            elif state == S3 and data == 1:
                next_state = S4
                next_out = 1
            else:
                # R4/R5: continue searching, output 0
                next_out = 0
                if state == S0:
                    next_state = S1 if data == 1 else S0
                elif state == S1:
                    next_state = S2 if data == 1 else S0
                elif state == S2:
                    next_state = S3 if data == 0 else S2
                elif state == S3:
                    # data == 0 here (data==1 handled above)
                    next_state = S1 if data == 1 else S0
                else:
                    next_state = S0

        # Output visible same cycle (registered output reflects new value)
        start_shifting = next_out
        state = next_state

        results.append({"start_shifting": start_shifting & 1})

    return results
