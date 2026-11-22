def reference(vectors):
    # State encoding
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4

    state = S0
    start_shifting = 0  # deterministic initial value (0); candidate allows 1 but we choose 0
    cur_reset = 0
    cur_data = 0
    results = []

    for row in vectors:
        # Apply row's driven input values before the sampled posedge
        if 'reset' in row:
            cur_reset = row['reset'] & 1
        if 'data' in row:
            cur_data = row['data'] & 1

        # Sample at posedge
        if cur_reset == 1:
            # r_reset_clear: reset == 1 forces synchronous clear
            next_state = S0
            next_start = 0
        else:
            # Next state logic
            if state == S0:
                if cur_data == 1:
                    next_state = S1
                else:
                    next_state = S0
            elif state == S1:
                if cur_data == 1:
                    next_state = S11
                else:
                    next_state = S0
            elif state == S11:
                if cur_data == 0:
                    next_state = S110
                else:
                    next_state = S11
            elif state == S110:
                if cur_data == 1:
                    next_state = FOUND
                else:
                    next_state = S0
            elif state == FOUND:
                next_state = FOUND
            else:
                next_state = S0

            # r_set_or_hold: set start_shifting to 1 when 1101 completes and hold in FOUND
            if state == FOUND or (state == S110 and cur_data == 1):
                next_start = 1
            else:
                # r_default_clear: start_shifting is 0 before detection (deterministic choice)
                next_start = 0

        # Update registers after posedge
        state = next_state
        start_shifting = next_start
        results.append({'start_shifting': start_shifting & 1})

        # Apply mid changes after sampling (carried to next row's pre-edge)
        if 'mid' in row:
            mid = row['mid']
            if mid:
                if 'reset' in mid:
                    cur_reset = mid['reset'] & 1
                if 'data' in mid:
                    cur_data = mid['data'] & 1

    return results
