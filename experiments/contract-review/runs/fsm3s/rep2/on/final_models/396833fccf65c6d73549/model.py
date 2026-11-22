def reference(vectors):
    # Rule global: Before the first reset, state is unspecified. We choose 'A' as a concrete arbitrary state.
    state = 'A'
    current_in = 0
    current_reset = 0
    results = []
    for row in vectors:
        # Drive row's values before the sampled posedge.
        if 'in' in row:
            current_in = row['in']
        if 'reset' in row:
            current_reset = row['reset']
        # Rule sync_reset: At posedge, if reset == 1 then state becomes A regardless of in.
        if current_reset == 1:
            state = 'A'
        else:
            # Rule transition_and_moore_output: explicit state transitions.
            if state == 'A':
                if current_in == 0:
                    state = 'A'
                else:
                    state = 'B'
            elif state == 'B':
                if current_in == 0:
                    state = 'C'
                else:
                    state = 'B'
            elif state == 'C':
                if current_in == 0:
                    state = 'A'
                else:
                    state = 'D'
            elif state == 'D':
                if current_in == 0:
                    state = 'C'
                else:
                    state = 'B'
        # Rule transition_and_moore_output: Moore output based on new state.
        if state == 'D':
            out = 1
        else:
            out = 0
        results.append({'out': out})
        # Process optional mid input changes AFTER sampling, carried to the start of the next row.
        if 'mid' in row:
            mid = row['mid']
            if 'in' in mid:
                current_in = mid['in']
            if 'reset' in mid:
                current_reset = mid['reset']
        if 'in_mid' in row:
            current_in = row['in_mid']
        if 'reset_mid' in row:
            current_reset = row['reset_mid']
    return results
