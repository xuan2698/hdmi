def reference(vectors):
    # global: State A at time zero per provided interpretation.
    state = 'A'
    cur_in = 0
    cur_reset = 0
    result = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        if 'in' in row:
            cur_in = row['in']
        if 'reset' in row:
            cur_reset = row['reset']

        # sync_reset: At posedge, reset == 1 forces state A regardless of in;
        # Moore output after the edge is 0.
        # transition_and_moore_output: With reset == 0, update state by the
        # specified table and derive out from the resulting state.
        if cur_reset == 1:
            state = 'A'
        else:
            if state == 'A':
                if cur_in == 0:
                    state = 'A'
                else:
                    state = 'B'
            elif state == 'B':
                if cur_in == 0:
                    state = 'C'
                else:
                    state = 'B'
            elif state == 'C':
                if cur_in == 0:
                    state = 'A'
                else:
                    state = 'D'
            else:  # state == 'D'
                if cur_in == 0:
                    state = 'C'
                else:
                    state = 'B'

        # Moore output is 1 only in state D.
        if state == 'D':
            out_val = 1
        else:
            out_val = 0
        result.append({'out': out_val})

        # mid: Optional mid input changes occur AFTER sampling, before the
        # other edge, and are carried to the start of the next row.
        if 'mid' in row:
            mid = row['mid']
            if mid is not None:
                if 'in' in mid:
                    cur_in = mid['in']
                if 'reset' in mid:
                    cur_reset = mid['reset']

        # Support alternative mid key spellings while preserving timing.
        if 'mid_in' in row:
            cur_in = row['mid_in']
        if 'in_mid' in row:
            cur_in = row['in_mid']
        if 'mid_reset' in row:
            cur_reset = row['mid_reset']
        if 'reset_mid' in row:
            cur_reset = row['reset_mid']

    return result
