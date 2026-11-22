def reference(vectors):
    # Initial concrete state: A (power-up unspecified, but choose reset state)
    state = 'A'
    inputs = {'in': 0, 'reset': 0}
    outputs = []

    for row in vectors:
        # Drive row values before the sampled posedge
        if 'in' in row:
            inputs['in'] = row['in'] & 1
        if 'reset' in row:
            inputs['reset'] = row['reset'] & 1

        rst = inputs['reset']
        in_val = inputs['in']

        # R_RESET: apply candidate interpretation for update_during_reset
        # During reset, B/C/D hold current state; only A updates (stays A).
        if rst == 1:
            if state == 'A':
                next_state = 'A'
            else:
                next_state = state
        else:
            # Explicit state transitions from the transition table
            if state == 'A':
                next_state = 'A' if in_val == 0 else 'B'
            elif state == 'B':
                next_state = 'C' if in_val == 0 else 'B'
            elif state == 'C':
                next_state = 'A' if in_val == 0 else 'D'
            elif state == 'D':
                next_state = 'C' if in_val == 0 else 'B'
            else:
                next_state = 'A'

        state = next_state

        # R_OUT_A, R_OUT_B, R_OUT_C, R_OUT_D: Moore output based on settled state
        if state == 'D':
            out_val = 1
        else:
            out_val = 0  # A, B, C all output 0

        outputs.append({'out': out_val & 1})

        # Process optional mid input changes after sampling; carry to next row
        if 'mid' in row:
            mid = row['mid']
            for k in mid:
                if k == 'in':
                    inputs['in'] = mid[k] & 1
                elif k == 'reset':
                    inputs['reset'] = mid[k] & 1
        # Also support flat mid keys if present
        if 'mid_in' in row:
            inputs['in'] = row['mid_in'] & 1
        if 'mid_reset' in row:
            inputs['reset'] = row['mid_reset'] & 1

    return outputs
