def reference(vectors):
    # Initial state: A (reset state, carry=0), power-up assumed concrete A
    state = 'A'
    cur_areset = 0
    cur_x = 0
    out = []

    for row in vectors:
        # Each row's values are driven before the sampled posedge edge
        if 'areset' in row:
            cur_areset = row['areset'] & 1
        if 'x' in row:
            cur_x = row['x'] & 1

        # async_reset: areset asserted high forces state A and z=0 independent of clk
        if cur_areset:
            state = 'A'

        # serial_twos_complement: posedge clk updates Moore state when areset=0
        if cur_areset == 0:
            if state == 'A':
                if cur_x == 0:
                    state = 'A'
                else:
                    state = 'B'
            elif state == 'B':
                if cur_x == 0:
                    state = 'B'
                else:
                    state = 'C'
            elif state == 'C':
                if cur_x == 0:
                    state = 'B'
                else:
                    state = 'C'

        # Moore output after settled posedge
        if state == 'A' or state == 'C':
            z = 0
        else:  # state == 'B'
            z = 1
        out.append({'z': z})

        # mid changes occur after sampling, carried to start of next row
        if 'mid' in row:
            mid = row['mid']
            if 'areset' in mid:
                cur_areset = mid['areset'] & 1
                # async_reset: mid assertion resets state immediately
                if cur_areset:
                    state = 'A'
            if 'x' in mid:
                cur_x = mid['x'] & 1

    return out
