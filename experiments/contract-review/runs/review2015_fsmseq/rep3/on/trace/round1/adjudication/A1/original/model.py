def reference(vectors):
    # State encoding: S0=0, S1=1, S2=2, S3=3, S4=4
    state = 0
    # Carried input values (updated by mid changes after each sampled posedge)
    cur = {'reset': 0, 'data': 0}
    out = []
    for row in vectors:
        # Apply this row's pre-edge input values, which override any carried mid values.
        if 'reset' in row:
            cur['reset'] = row['reset']
        if 'data' in row:
            cur['data'] = row['data']
        reset = cur['reset']
        data = cur['data']
        # Compute next state on posedge clk
        if reset == 1:
            # R1_reset_clear: synchronous active-high reset forces S0 and start_shifting=0
            nxt = 0
        else:
            if state == 0:
                nxt = 1 if data == 1 else 0
            elif state == 1:
                nxt = 2 if data == 1 else 0
            elif state == 2:
                nxt = 2 if data == 1 else 3
            elif state == 3:
                # R2_detect_set_and_hold: S3 + data==1 -> S4 (start_shifting=1)
                # R3_default_zero_while_searching: S3 + data==0 -> S0
                nxt = 4 if data == 1 else 0
            else:  # state == 4
                # R2_detect_set_and_hold: S4 holds start_shifting=1 for any data while reset==0
                nxt = 4
        state = nxt
        # Output after posedge: start_shifting=1 iff in S4 (detected and holding)
        start_shifting = 1 if state == 4 else 0
        out.append({'start_shifting': start_shifting})
        # Process mid changes after sampling, carried to next row's start.
        mid = row.get('mid')
        if mid:
            for k, v in mid.items():
                cur[k] = v
    return out
