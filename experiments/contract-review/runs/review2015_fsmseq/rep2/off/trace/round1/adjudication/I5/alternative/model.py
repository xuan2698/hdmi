def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0)
        data = row.get('data', 0)

        # R1: reset == 1 -> start_shifting = 0 (sync, same cycle visible)
        if reset == 1:
            start_shifting = 0
            state = S0
            out.append({'start_shifting': start_shifting})
            continue

        # Compute next state and output based on current state and data
        # R2: state == S4 -> start_shifting stays 1
        # R3: state == S3 and data == 1 -> start_shifting = 1
        # R4: otherwise start_shifting = 0
        if state == S4:
            # R2
            start_shifting = 1
            # global: FSM continues searching after match; re-enter on new patterns
            if data == 1:
                state = S1
            else:
                state = S0
        elif state == S3 and data == 1:
            # R3
            start_shifting = 1
            state = S4
        else:
            # R4
            start_shifting = 0
            # transition logic for searching 1101
            if state == S0:
                state = S1 if data == 1 else S0
            elif state == S1:
                state = S2 if data == 1 else S0
            elif state == S2:
                state = S3 if data == 0 else S2
            elif state == S3:
                # data == 0 here (since data==1 handled above)
                state = S0
            else:
                state = S0

        out.append({'start_shifting': start_shifting})

    return out
