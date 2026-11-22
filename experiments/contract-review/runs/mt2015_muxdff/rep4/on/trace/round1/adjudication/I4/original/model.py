def reference(vectors):
    # State: Q is the registered output; state holds last driven inputs.
    Q = 0
    state = {'L': 0, 'q_in': 0, 'r_in': 0}
    out = []

    for row in vectors:
        # Determine input values at this sampled posedge: previous state overridden by row values.
        L = state['L']
        q_in = state['q_in']
        r_in = state['r_in']

        if 'L' in row:
            L = row['L']
        if 'q_in' in row:
            q_in = row['q_in']
        if 'r_in' in row:
            r_in = row['r_in']

        L = L & 1
        q_in = q_in & 1
        r_in = r_in & 1

        state['L'] = L
        state['q_in'] = q_in
        state['r_in'] = r_in

        # Q_posedge_update: At posedge clk after settlement, Q becomes r_in when L=1; otherwise Q becomes q_in.
        if L:
            Q = r_in
        else:
            Q = q_in

        Q = Q & 1
        out.append({'Q': Q})

        # Mid changes occur after sampling and before the next edge; they carry to the next row.
        if 'mid' in row:
            mid = row['mid']
            if mid is not None:
                try:
                    if 'L' in mid:
                        state['L'] = mid['L'] & 1
                    if 'q_in' in mid:
                        state['q_in'] = mid['q_in'] & 1
                    if 'r_in' in mid:
                        state['r_in'] = mid['r_in'] & 1
                except:
                    pass

        # Also support explicit mid_* / *_mid keys if present.
        if 'mid_L' in row:
            state['L'] = row['mid_L'] & 1
        if 'mid_q_in' in row:
            state['q_in'] = row['mid_q_in'] & 1
        if 'mid_r_in' in row:
            state['r_in'] = row['mid_r_in'] & 1
        if 'L_mid' in row:
            state['L'] = row['L_mid'] & 1
        if 'q_in_mid' in row:
            state['q_in'] = row['q_in_mid'] & 1
        if 'r_in_mid' in row:
            state['r_in'] = row['r_in_mid'] & 1

    return out
