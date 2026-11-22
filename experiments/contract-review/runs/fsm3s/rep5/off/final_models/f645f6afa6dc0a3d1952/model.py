def reference(vectors):
    # Contract implementation.
    # State encoding: A=0, B=1, C=2, D=3
    # R1: out=0 when state in {A,B,C} (combinational, same_cycle)
    # R2: out=1 when state == D (combinational, same_cycle)
    # R3: sync active-high reset forces state A at posedge (next_cycle)
    # R4: A: in=0->A, in=1->B (posedge, next_cycle)
    # R5: B: in=0->C, in=1->B (posedge, next_cycle)
    # R6: C: in=0->A, in=1->D (posedge, next_cycle)
    # R7: D: in=0->C, in=1->B (posedge, next_cycle)
    # Mid changes: applied after sampling, carried to next row.

    state = 0  # power-up unspecified; start at A
    results = []
    pending = None  # mid input change carried to next row

    for row in vectors:
        # Apply carried mid change from previous row before sampling
        if pending is not None:
            row = dict(row)
            row.update(pending)
            pending = None

        in_val = row.get('in', 0) & 1
        reset_val = row.get('reset', 0) & 1

        # R1 / R2: combinational output based on current state
        if state == 3:  # D
            out_val = 1  # R2
        else:
            out_val = 0  # R1

        results.append({'out': out_val})

        # Compute next state at posedge
        if reset_val == 1:
            # R3: sync active-high reset -> A
            next_state = 0
        else:
            if state == 0:  # A
                next_state = 1 if in_val == 1 else 0  # R4
            elif state == 1:  # B
                next_state = 1 if in_val == 1 else 2  # R5
            elif state == 2:  # C
                next_state = 3 if in_val == 1 else 0  # R6
            else:  # D
                next_state = 1 if in_val == 1 else 2  # R7

        state = next_state

        # Handle optional mid input change (after sampling, before next edge)
        if 'mid' in row and row['mid'] is not None:
            pending = row['mid']

    return results
