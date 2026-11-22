def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Power-up state (unspecified, choose S0)
    state = S0
    start_shifting = 0

    outputs = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # R1: reset == 1 -> start_shifting = 0 (priority 1)
        # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
        # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1 (priority 3)
        # R4: reset == 0 and state != S4 and not (state == S3 and data == 1) -> start_shifting = 0 (priority 4)
        if reset == 1:
            # R1
            start_shifting = 0
            state = S0
        else:
            if state == S4:
                # R2
                start_shifting = 1
                state = S4
            elif state == S3 and data == 1:
                # R3
                start_shifting = 1
                state = S4
            else:
                # R4
                start_shifting = 0
                # Explicit transitions
                if state == S0:
                    state = S1 if data == 1 else S0
                elif state == S1:
                    state = S2 if data == 1 else S0
                elif state == S2:
                    state = S3 if data == 0 else S2
                elif state == S3:
                    # data == 0 here (data == 1 handled above)
                    state = S1 if data == 1 else S0
                else:
                    state = S0

        outputs.append({'start_shifting': start_shifting & 1})

    return outputs
