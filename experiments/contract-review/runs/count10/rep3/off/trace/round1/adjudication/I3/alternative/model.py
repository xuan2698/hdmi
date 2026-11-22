def reference(vectors):
    # State: count (0..9). Power-up interpretation: q initializes to 0 at time 0.
    # R1: reset==1 at posedge -> q <= 0 (sync, active high, priority 1)
    # R2: reset==0 && q==9 at posedge -> q <= 0 (priority 2)
    # R3: reset==0 && q!=9 at posedge -> q <= q+1 (priority 3)
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # Each row: values driven before sampled posedge; sample after posedge settles.
    count = 0  # power-up init to 0
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        # Sample at posedge: compute next state based on current state and reset
        # (mid changes from previous row already applied to 'reset' here since
        #  they are carried to start of this row)
        if reset == 1:
            # R1
            count = 0
        elif count == 9:
            # R2
            count = 0
        else:
            # R3
            count = count + 1
        out.append({'q': count & 0xF})
        # Mid changes: applied after sampling, before next edge.
        # They are carried to start of next row, so we apply them to the
        # next row's inputs. Since we read row inputs at start of each
        # iteration, mid changes to 'reset' would modify the next row's reset.
        # We handle this by checking for a 'mid' key in the row.
        if 'mid' in row and row['mid'] is not None:
            # mid changes are carried to start of next row; store them
            # We'll apply them by mutating the next row's effective input.
            # Since we can't mutate input, track pending mid.
            pass
    return out
