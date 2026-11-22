def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # R1: reset == 1 -> start_shifting = 0 (priority 1)
        # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
        # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1 (priority 3)
        # R4: otherwise -> start_shifting = 0 (priority 4)
        if reset == 1:
            start_shifting = 0
        elif state == S4:
            start_shifting = 1
        elif state == S3 and data == 1:
            start_shifting = 1
        else:
            start_shifting = 0

        out.append({'start_shifting': start_shifting})

        # State update at posedge (after sampling)
        if reset == 1:
            state = S0
        else:
            if state == S0:
                state = S1 if data == 1 else S0
            elif state == S1:
                state = S2 if data == 1 else S0
            elif state == S2:
                state = S3 if data == 0 else S2
            elif state == S3:
                state = S4 if data == 1 else S0
            elif state == S4:
                state = S4

    return out
