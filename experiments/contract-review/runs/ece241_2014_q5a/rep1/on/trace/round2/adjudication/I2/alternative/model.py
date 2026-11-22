def reference(vectors):
    # Initial state A (reset state), output z=0.
    # Power-up is unspecified, but concrete starting state A gives z=0.
    state = 'A'
    z = 0
    # Current input values, initialized to reset asserted and x=0.
    cur_areset = 1
    cur_x = 0
    results = []
    for row in vectors:
        # Row values are driven before the sampled edge.
        # If a key is missing, the value carried from a previous mid change remains.
        if 'areset' in row:
            cur_areset = row['areset']
        if 'x' in row:
            cur_x = row['x']

        # Process the sampled posedge.
        # reset_async_z0 (candidate interpretation): areset==1 holds the last state and output.
        if cur_areset == 1:
            # Hold state and z unchanged.
            pass
        else:
            # areset==0: normal transitions and output based on next state.
            if state == 'A':
                # A_x0_to_A_z0
                if cur_x == 0:
                    state = 'A'
                    z = 0
                # A_x1_to_C_z1
                else:
                    state = 'C'
                    z = 1
            elif state == 'B':
                # B_x0_to_C_z1
                if cur_x == 0:
                    state = 'C'
                    z = 1
                # B_x1_to_B_z0
                else:
                    state = 'B'
                    z = 0
            elif state == 'C':
                # C_x0_to_C_z1
                if cur_x == 0:
                    state = 'C'
                    z = 1
                # C_x1_to_B_z0
                else:
                    state = 'B'
                    z = 0

        # Output visible after the posedge has settled.
        results.append({'z': z})

        # Optional mid input changes occur after sampling and persist to the next row.
        if 'mid' in row:
            mid = row['mid']
            if 'areset' in mid:
                cur_areset = mid['areset']
            if 'x' in mid:
                cur_x = mid['x']

    return results
