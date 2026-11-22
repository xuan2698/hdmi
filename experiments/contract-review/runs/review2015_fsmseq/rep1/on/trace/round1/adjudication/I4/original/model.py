def reference(vectors):
    # State encodings
    S0 = 0
    S1 = 1
    S11 = 2
    S110 = 3
    FOUND = 4

    state = S0
    current = {'reset': 0, 'data': 0}
    result = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        # Mid changes from the previous row are already in current and are
        # overwritten here if the row explicitly drives the same input.
        if 'reset' in row:
            current['reset'] = row['reset'] & 1
        if 'data' in row:
            current['data'] = row['data'] & 1

        reset = current['reset']
        data = current['data']

        # R_RESET: reset == 1 at posedge forces S0 and start_shifting=0
        if reset:
            next_state = S0
            start_shifting = 0
        else:
            # Explicit state transitions
            if state == S0:
                next_state = S1 if data else S0
            elif state == S1:
                next_state = S11 if data else S0
            elif state == S11:
                next_state = S11 if data else S110
            elif state == S110:
                if data:
                    next_state = FOUND  # R_COMPLETE_1101
                else:
                    next_state = S0
            elif state == FOUND:
                next_state = FOUND      # R_HOLD_FOUND
            else:
                next_state = S0

            # R_COMPLETE_1101, R_HOLD_FOUND, R_ZERO_NOT_FOUND:
            # start_shifting is 1 exactly when the state after the posedge is FOUND.
            start_shifting = 1 if next_state == FOUND else 0

        # Update state after the sampled posedge
        state = next_state

        # Output visible after the posedge has settled
        result.append({'start_shifting': start_shifting})

        # Optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row.
        mid = row.get('mid')
        if mid:
            if 'reset' in mid:
                current['reset'] = mid['reset'] & 1
            if 'data' in mid:
                current['data'] = mid['data'] & 1

    return result
