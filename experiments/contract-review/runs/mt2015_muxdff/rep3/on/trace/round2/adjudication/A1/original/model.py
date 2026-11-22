def reference(vectors):
    # Initialize current input values (carried mid changes). Default 0.
    cur_L = 0
    cur_q_in = 0
    cur_r_in = 0
    Q = 0
    result = []
    for v in vectors:
        # Apply explicit inputs driven before posedge.
        if 'L' in v:
            cur_L = v['L'] & 1
        if 'q_in' in v:
            cur_q_in = v['q_in'] & 1
        if 'r_in' in v:
            cur_r_in = v['r_in'] & 1
        # Compute registered output at posedge.
        if cur_L == 1:
            Q = cur_r_in  # rule load_r: L==1 -> Q = r_in
        else:
            Q = cur_q_in  # rule hold_q_in: L==0 -> Q = q_in
        result.append({'Q': Q & 1})
        # Apply optional mid input changes after sampling, carried to next row.
        mid = v.get('mid')
        if mid is not None:
            for k in mid:
                if k == 'L':
                    cur_L = mid[k] & 1
                elif k == 'q_in':
                    cur_q_in = mid[k] & 1
                elif k == 'r_in':
                    cur_r_in = mid[k] & 1
    return result
