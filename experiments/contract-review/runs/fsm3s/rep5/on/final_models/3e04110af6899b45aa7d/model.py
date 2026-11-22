def reference(vectors):
    state = 0  # 0=A, 1=B, 2=C, 3=D; power-up concrete default A
    cur_in = 0
    cur_reset = 0
    results = []
    for row in vectors:
        # Primary inputs are driven before the sampled posedge
        try:
            cur_in = row['in']
        except:
            pass
        try:
            cur_reset = row['reset']
        except:
            pass

        # Synchronous active-high reset and posedge state update
        if cur_reset == 1:
            state = 0  # reset_to_A
        else:
            if state == 0:      # A
                if cur_in == 0:
                    state = 0   # A in=0 -> A
                else:
                    state = 1   # A in=1 -> B
            elif state == 1:    # B
                if cur_in == 0:
                    state = 2   # B in=0 -> C
                else:
                    state = 1   # B in=1 -> B
            elif state == 2:    # C
                if cur_in == 0:
                    state = 0   # C in=0 -> A
                else:
                    state = 3   # C in=1 -> D
            elif state == 3:    # D
                if cur_in == 0:
                    state = 2   # D in=0 -> C
                else:
                    state = 1   # D in=1 -> B

        # Moore output based on new state, visible same cycle
        if state == 0:
            out = 0  # out_A
        elif state == 1:
            out = 0  # out_B
        elif state == 2:
            out = 0  # out_C
        else:
            out = 1  # out_D
        results.append({'out': out})

        # Optional mid input changes occur AFTER sampling,
        # carried to the start of the next row.
        try:
            mid = row['mid']
            for k in mid:
                if k == 'in':
                    cur_in = mid[k]
                elif k == 'reset':
                    cur_reset = mid[k]
        except:
            pass
        # Alternate mid representation: keys like 'in_mid'
        try:
            for k in row:
                if k == 'in_mid':
                    cur_in = row[k]
                elif k == 'reset_mid':
                    cur_reset = row[k]
        except:
            pass
    return results
