def reference(vectors):
    # State encoding: 0=S0, 1=S1, 2=S2, 3=S3, 4=S4
    state = 0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0)
        data = row.get('data', 0)

        # R1: reset == 1 -> start_shifting = 0 (priority 1)
        if reset == 1:
            state = 0
            start_shifting = 0
            out.append({'start_shifting': start_shifting})
            continue

        # Compute next state from current state and data
        if state == 0:
            nxt = 1 if data == 1 else 0
        elif state == 1:
            nxt = 2 if data == 1 else 0
        elif state == 2:
            nxt = 3 if data == 0 else 2
        elif state == 3:
            nxt = 4 if data == 1 else 1
        else:  # state == 4
            nxt = 4

        # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
        # R3: reset == 0 and state != S4 and next_state == S4 -> start_shifting = 1 (priority 3)
        # R4: reset == 0 and state != S4 and next_state != S4 -> start_shifting = 0 (priority 4)
        if state == 4:
            start_shifting = 1
        elif nxt == 4:
            start_shifting = 1
        else:
            start_shifting = 0

        state = nxt
        out.append({'start_shifting': start_shifting})

    return out
