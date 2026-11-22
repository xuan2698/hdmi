def reference(vectors):
    # State encoding: 0=S0, 1=S1, 2=S2, 3=S3, 4=SF
    state = 0
    current_reset = 0
    current_data = 0
    result = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        if 'reset' in row:
            current_reset = row['reset']
        if 'data' in row:
            current_data = row['data']

        # Sample at posedge.
        if current_reset == 1:
            # R_RESET: reset == 1 at sampled posedge; state <= S0, start_shifting <= 0
            out = 0
            next_state = 0
        else:
            if state == 4:
                # R_HOLD: reset == 0 and current state == SF; next state <= SF, start_shifting <= 1
                out = 1
                next_state = 4
            elif state == 3:
                if current_data == 1:
                    # R_DETECT: reset == 0, state == S3, data == 1; next state <= SF, start_shifting <= 1
                    out = 1
                    next_state = 4
                else:
                    # R_PROGRESS: S3 + 0 -> S0; start_shifting <= 0
                    out = 0
                    next_state = 0
            elif state == 2:
                if current_data == 1:
                    # R_PROGRESS: S2 + 1 -> S2
                    out = 0
                    next_state = 2
                else:
                    # R_PROGRESS: S2 + 0 -> S3
                    out = 0
                    next_state = 3
            elif state == 1:
                if current_data == 1:
                    # R_PROGRESS: S1 + 1 -> S2
                    out = 0
                    next_state = 2
                else:
                    # R_PROGRESS: S1 + 0 -> S0
                    out = 0
                    next_state = 0
            else:  # state == 0
                if current_data == 1:
                    # R_PROGRESS: S0 + 1 -> S1
                    out = 0
                    next_state = 1
                else:
                    # R_PROGRESS: S0 + 0 -> S0
                    out = 0
                    next_state = 0

        result.append({'start_shifting': out})
        state = next_state

        # Optional mid input changes occur AFTER sampling and persist to the next row.
        if 'mid' in row:
            mid = row['mid']
            if 'reset' in mid:
                current_reset = mid['reset']
            if 'data' in mid:
                current_data = mid['data']

    return result
