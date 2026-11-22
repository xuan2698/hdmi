def reference(vectors):
    # State encoding: 0=S0, 1=S1, 2=S11, 3=S110, 4=FOUND
    state = 0
    cur_reset = 0
    cur_data = 0
    result = []

    for row in vectors:
        # Drive row values before the sampled posedge.
        if 'reset' in row:
            cur_reset = int(row['reset']) & 1
        if 'data' in row:
            cur_data = int(row['data']) & 1

        # Synchronous active-high reset has priority at posedge.
        if cur_reset == 1:
            next_state = 0  # S0
            start_shifting = 0  # r_reset_clear
        else:
            # Explicit named-state transitions.
            if state == 0:  # S0
                next_state = 1 if cur_data else 0
            elif state == 1:  # S1
                next_state = 2 if cur_data else 0
            elif state == 2:  # S11
                next_state = 2 if cur_data else 3
            elif state == 3:  # S110
                next_state = 4 if cur_data else 0
            else:  # FOUND
                next_state = 4

            if next_state == 4:
                start_shifting = 1  # r_set_or_hold
            else:
                start_shifting = 0  # r_default_clear

        result.append({'start_shifting': start_shifting & 1})
        state = next_state

        # Optional mid changes occur after the posedge sample and carry forward.
        if 'mid' in row and row['mid'] is not None:
            mid = row['mid']
            if 'reset' in mid:
                cur_reset = int(mid['reset']) & 1
            if 'data' in mid:
                cur_data = int(mid['data']) & 1

    return result
