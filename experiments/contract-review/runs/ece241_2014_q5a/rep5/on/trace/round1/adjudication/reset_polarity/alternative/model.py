def reference(vectors):
    # async_reset_assert: active-low areset asserted at 0 forces state A and z=0.
    state = 'A'
    cur_areset = 0
    cur_x = 0
    result = []
    for row in vectors:
        # Inputs driven before the sampled posedge; explicit row values override carried mid changes.
        if 'areset' in row:
            cur_areset = row['areset']
        if 'x' in row:
            cur_x = row['x']

        # Asynchronous reset: active-low, asserted when cur_areset == 0.
        # async_reset_assert
        if cur_areset == 0:
            state = 'A'

        # Sample after posedge has settled.
        if cur_areset == 0:
            # async_reset_assert
            state = 'A'
            z = 0
        else:
            if state == 'A':
                if cur_x == 0:
                    # A_on_x0
                    state = 'A'
                    z = 0
                else:
                    # A_on_x1
                    state = 'B'
                    z = 1
            elif state == 'B':
                if cur_x == 0:
                    # B_on_x0
                    state = 'B'
                    z = 1
                else:
                    # B_on_x1
                    state = 'C'
                    z = 0
            else:
                if cur_x == 0:
                    # C_on_x0
                    state = 'B'
                    z = 1
                else:
                    # C_on_x1
                    state = 'C'
                    z = 0

        result.append({'z': z})

        # Optional mid changes occur AFTER sampling and are carried to the next row.
        if 'mid' in row:
            mid = row['mid']
            if mid:
                if 'areset' in mid:
                    cur_areset = mid['areset']
                if 'x' in mid:
                    cur_x = mid['x']
                # async_reset_assert
                if cur_areset == 0:
                    state = 'A'

    return result
