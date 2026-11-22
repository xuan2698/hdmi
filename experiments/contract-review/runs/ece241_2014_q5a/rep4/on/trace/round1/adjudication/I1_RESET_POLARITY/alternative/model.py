def reference(vectors):
    # R_RESET: active-low asynchronous reset; areset==0 asserts reset, forcing START and z=0.
    state = 0  # 0=START, 1=INV0, 2=INV1
    cur_areset = 1
    cur_x = 0
    out = []
    for row in vectors:
        if 'areset' in row:
            cur_areset = row['areset']
        if 'x' in row:
            cur_x = row['x']

        if cur_areset == 0:
            state = 0
            z = 0
        else:
            # R_CONVERT: posedge samples x and updates the serial 2's-complement Moore state.
            if state == 0:
                if cur_x == 0:
                    state = 0
                else:
                    state = 2
            elif state == 1:
                if cur_x == 0:
                    state = 2
                else:
                    state = 1
            else:
                if cur_x == 0:
                    state = 2
                else:
                    state = 1
            if state == 2:
                z = 1
            else:
                z = 0

        out.append({'z': z})

        if 'mid' in row:
            mid = row['mid']
            if 'areset' in mid:
                cur_areset = mid['areset']
                if cur_areset == 0:
                    # R_RESET: asynchronous assertion after sampling resets state for the next sampled edge.
                    state = 0
            if 'x' in mid:
                cur_x = mid['x']

    return out
