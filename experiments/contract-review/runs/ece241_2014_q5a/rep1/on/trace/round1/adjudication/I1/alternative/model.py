def reference(vectors):
    # Moore state machine for a serial 2's complementer.
    # Candidate override: areset is active-low (reset asserted when areset == 0),
    # and z = 0 during reset. State A is the reset/no-first-1 state.
    state = 'A'
    cur_areset = 1
    cur_x = 0
    results = []

    for row in vectors:
        # Inputs are driven before the sampled posedge.
        if 'areset' in row:
            cur_areset = row['areset']
        if 'x' in row:
            cur_x = row['x']

        # reset_async_z0: areset active-low, asynchronous reset forces A and z=0.
        if cur_areset == 0:
            state = 'A'

        if cur_areset == 0:
            # reset_async_z0: output during reset is 0.
            state = 'A'
            z = 0
        else:
            # Normal posedge transitions when reset is released (areset == 1).
            if state == 'A':
                if cur_x == 0:
                    # A_x0_to_A_z0
                    state = 'A'
                else:
                    # A_x1_to_C_z1
                    state = 'C'
            elif state == 'B':
                if cur_x == 0:
                    # B_x0_to_C_z1
                    state = 'C'
                else:
                    # B_x1_to_B_z0
                    state = 'B'
            else:  # state == 'C'
                if cur_x == 0:
                    # C_x0_to_C_z1
                    state = 'C'
                else:
                    # C_x1_to_B_z0
                    state = 'B'

            # Moore output after the sampled posedge has settled.
            if state == 'A':
                z = 0
            elif state == 'B':
                z = 0
            else:  # state == 'C'
                z = 1

        results.append({'z': z})

        # Optional mid changes occur after sampling and are carried to next row.
        if 'mid' in row:
            m = row['mid']
            try:
                for k in m:
                    v = m[k]
                    if k == 'areset':
                        cur_areset = v
                        if v == 0:
                            # reset_async_z0: asynchronous reset assertion forces A.
                            state = 'A'
                    elif k == 'x':
                        cur_x = v
            except:
                for change in m:
                    try:
                        for k in change:
                            v = change[k]
                            if k == 'areset':
                                cur_areset = v
                                if v == 0:
                                    state = 'A'
                            elif k == 'x':
                                cur_x = v
                    except:
                        k = change[0]
                        v = change[1]
                        if k == 'areset':
                            cur_areset = v
                            if v == 0:
                                state = 'A'
                        elif k == 'x':
                            cur_x = v

        if 'mid_changes' in row:
            m = row['mid_changes']
            try:
                for k in m:
                    v = m[k]
                    if k == 'areset':
                        cur_areset = v
                        if v == 0:
                            state = 'A'
                    elif k == 'x':
                        cur_x = v
            except:
                for change in m:
                    try:
                        for k in change:
                            v = change[k]
                            if k == 'areset':
                                cur_areset = v
                                if v == 0:
                                    state = 'A'
                            elif k == 'x':
                                cur_x = v
                    except:
                        k = change[0]
                        v = change[1]
                        if k == 'areset':
                            cur_areset = v
                            if v == 0:
                                state = 'A'
                        elif k == 'x':
                            cur_x = v

        if 'mid_change' in row:
            m = row['mid_change']
            try:
                for k in m:
                    v = m[k]
                    if k == 'areset':
                        cur_areset = v
                        if v == 0:
                            state = 'A'
                    elif k == 'x':
                        cur_x = v
            except:
                for change in m:
                    try:
                        for k in change:
                            v = change[k]
                            if k == 'areset':
                                cur_areset = v
                                if v == 0:
                                    state = 'A'
                            elif k == 'x':
                                cur_x = v
                    except:
                        k = change[0]
                        v = change[1]
                        if k == 'areset':
                            cur_areset = v
                            if v == 0:
                                state = 'A'
                        elif k == 'x':
                            cur_x = v

        # reset_async_z0: if reset is asserted after mid changes, hold state A.
        if cur_areset == 0:
            state = 'A'

    return results
