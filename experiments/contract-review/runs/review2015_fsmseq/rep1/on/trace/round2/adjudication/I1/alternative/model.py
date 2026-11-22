def reference(vectors):
    # R_RESET: active-high synchronous reset forces state S0 and start_shifting=0 at posedge.
    # R_COMPLETE_1101: completion of 1101 goes to FOUND; start_shifting is registered and asserts on the following posedge.
    # R_HOLD_FOUND: once start_shifting is 1, hold it at 1 in FOUND until reset.
    # R_ZERO_NOT_FOUND: before detection, start_shifting remains 0.
    state = 'S0'
    start_shifting = 0
    current_reset = 0
    current_data = 0
    result = []

    for v in vectors:
        # Inputs driven before this sampled posedge. Explicit row values override carried values.
        reset = v.get('reset', current_reset)
        data = v.get('data', current_data)

        if reset == 1:
            # R_RESET
            next_state = 'S0'
            next_start = 0
        else:
            if start_shifting == 1:
                # R_HOLD_FOUND
                next_state = 'FOUND'
                next_start = 1
            else:
                if state == 'FOUND':
                    # R_HOLD_FOUND / R_COMPLETE_1101: registered output asserts one posedge after reaching FOUND.
                    next_state = 'FOUND'
                    next_start = 1
                elif state == 'S0':
                    # R_ZERO_NOT_FOUND
                    if data == 1:
                        next_state = 'S1'
                    else:
                        next_state = 'S0'
                    next_start = 0
                elif state == 'S1':
                    # R_ZERO_NOT_FOUND
                    if data == 1:
                        next_state = 'S11'
                    else:
                        next_state = 'S0'
                    next_start = 0
                elif state == 'S11':
                    # R_ZERO_NOT_FOUND
                    if data == 1:
                        next_state = 'S11'
                    else:
                        next_state = 'S110'
                    next_start = 0
                elif state == 'S110':
                    if data == 1:
                        # R_COMPLETE_1101: registered output, so start_shifting stays 0 on this completion posedge.
                        next_state = 'FOUND'
                        next_start = 0
                    else:
                        # R_ZERO_NOT_FOUND
                        next_state = 'S0'
                        next_start = 0
                else:
                    # Safety default, not expected.
                    next_state = 'S0'
                    next_start = 0

        state = next_state
        start_shifting = next_start
        result.append({'start_shifting': start_shifting})

        # Carry post-edge input values and apply any mid changes for the start of the next row.
        current_reset = reset
        current_data = data
        mid = v.get('mid', None)
        if mid:
            current_reset = mid.get('reset', current_reset)
            current_data = mid.get('data', current_data)

    return result
