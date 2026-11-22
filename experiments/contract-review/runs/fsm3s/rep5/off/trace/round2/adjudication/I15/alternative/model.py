def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R1: combinational output for A/B/C = 0
    # R2: combinational output for D = 1
    # R3: synchronous active high reset -> state A on posedge
    # R4-R7: posedge state transitions per table
    # Mid changes occur AFTER sampling, before other edge, carried to next row start.

    state = 0  # power-up unspecified; start at A (reset state)
    out = 0
    results = []

    for row in vectors:
        # Apply any mid changes carried from previous row (already applied to state? no)
        # Mid changes are input changes that occur after sampling; they affect the
        # input value seen at the next posedge. We model by updating 'in' after
        # sampling for the current row, before next row's sample.
        # Since vectors provide 'in' per row, we treat row['in'] as the value
        # driven before the sampled edge for this row. Mid changes from previous
        # row would have been applied to 'in' already if we tracked them; here
        # we simply use row['in'] as the sampled value.

        in_val = row.get('in', 0)
        reset_val = row.get('reset', 0)

        # R1/R2: combinational output based on current state (before edge)
        if state == 3:  # D
            out = 1  # R2
        else:  # A, B, C
            out = 0  # R1

        results.append({'out': out})

        # R3: synchronous reset takes priority on posedge
        if reset_val == 1:
            state = 0  # A
        else:
            # R4-R7: state transitions
            if state == 0:  # A
                state = 0 if in_val == 0 else 1  # R4
            elif state == 1:  # B
                state = 2 if in_val == 0 else 1  # R5
            elif state == 2:  # C
                state = 0 if in_val == 0 else 3  # R6
            elif state == 3:  # D
                state = 2 if in_val == 0 else 1  # R7

        # Mid changes: if a mid change occurred after sampling, it would update
        # 'in' for the next row. Since vectors supply per-row 'in', we assume
        # the next row's 'in' already reflects any mid change. No extra action.

    return results
