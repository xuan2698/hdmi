def reference(vectors):
    # sync_reset: implemented at posedge with reset priority
    # transition_and_moore_output: implemented state transition and Moore output
    # uncertain initial state: chosen as A
    state = 'A'
    cur_in = 0
    cur_reset = 0
    outs = []
    for row in vectors:
        # Drive row inputs before the sampled posedge
        if 'in' in row:
            cur_in = row['in']
        if 'reset' in row:
            cur_reset = row['reset']
        # At posedge: sync_reset has priority 100
        if cur_reset == 1:
            # sync_reset
            state = 'A'
        else:
            # transition_and_moore_output
            if state == 'A':
                if cur_in == 1:
                    state = 'B'
                else:
                    state = 'A'
            elif state == 'B':
                if cur_in == 1:
                    state = 'B'
                else:
                    state = 'C'
            elif state == 'C':
                if cur_in == 1:
                    state = 'D'
                else:
                    state = 'A'
            elif state == 'D':
                if cur_in == 1:
                    state = 'B'
                else:
                    state = 'C'
        # Moore output after edge
        if state == 'D':
            out_val = 1
        else:
            out_val = 0
        outs.append({'out': out_val})
        # Process optional mid changes after sampling, carry to next row
        if 'mid' in row:
            mid = row['mid']
            if 'in' in mid:
                cur_in = mid['in']
            if 'reset' in mid:
                cur_reset = mid['reset']
    return outs
