def reference(vectors):
    # r_posedge_q_sync_reset: At each positive clk edge, if reset==1, q <= 0;
    # otherwise q <= d. Synchronous active-high reset dominates the d load.
    q_reg = 0
    d_cur = 0
    reset_cur = 0
    result = []
    for row in vectors:
        if 'd' in row:
            d_cur = row['d']
        if 'reset' in row:
            reset_cur = row['reset']
        # Positive edge of clk has settled.
        if reset_cur == 1:
            q_reg = 0
        else:
            q_reg = d_cur & 255
        result.append({'q': q_reg})
        # Optional mid input changes occur after sampling, before next edge.
        if 'mid' in row:
            mid = row['mid']
            if 'd' in mid:
                d_cur = mid['d']
            if 'reset' in mid:
                reset_cur = mid['reset']
    return result
