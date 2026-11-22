def reference(vectors):
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    cur_reset = 0
    cur_data = 0
    result = []

    for row in vectors:
        # Pre-edge inputs: row values are driven before the sampled posedge.
        if 'reset' in row:
            cur_reset = row['reset']
        if 'data' in row:
            cur_data = row['data']

        if cur_reset == 1:
            # R1_reset_clear: synchronous reset forces state S0.
            # Candidate interpretation: start_shifting retains its pre-reset value.
            state = S0
        else:
            if state == S4 or (state == S3 and cur_data == 1):
                # R2_detect_set_and_hold: detection sets and holds start_shifting=1.
                state = S4
                start_shifting = 1
            else:
                # R3_default_zero_while_searching: default zero and 1101-prefix transitions.
                start_shifting = 0
                if state == S0:
                    state = S1 if cur_data == 1 else S0
                elif state == S1:
                    state = S2 if cur_data == 1 else S0
                elif state == S2:
                    state = S2 if cur_data == 1 else S3
                elif state == S3:
                    state = S0

        result.append({'start_shifting': int(start_shifting) & 1})

        # Mid changes occur after sampling and carry to the next row's pre-edge start.
        if 'mid' in row:
            mid = row['mid']
            if mid is not None:
                if 'reset' in mid:
                    cur_reset = mid['reset']
                if 'data' in mid:
                    cur_data = mid['data']

    return result
