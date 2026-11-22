def reference(vectors):
    # State: q is the single-bit D flip-flop output/state.
    q = 0
    d_cur = 0
    r_cur = 0
    out = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge.
        if 'd' in row:
            d_cur = row['d']
        if 'r' in row:
            r_cur = row['r']

        # sync_reset: at a sampled posedge, r == 1 forces q to 0 regardless of d.
        # d_load: at a sampled posedge, r == 0 makes q capture d.
        if r_cur == 1:
            q = 0
        else:
            q = d_cur & 1

        out.append({'q': q})

        # Mid changes occur AFTER sampling the posedge and are carried to the
        # start of the next row; they do not affect the already sampled q.
        mid = row.get('mid')
        if mid:
            if 'd' in mid:
                d_cur = mid['d']
            if 'r' in mid:
                r_cur = mid['r']

    return out
