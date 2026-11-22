def reference(vectors):
    # Moore FSM with synchronous active high reset to state A.
    state = 'A'  # initial state (reset state)
    outputs = []
    for row in vectors:
        # rule reset_high: synchronous active high reset forces state A
        if row.get('reset', 0) == 1:
            next_state = 'A'
        else:
            in_val = row.get('in', 0)
            if state == 'A':
                # rule state_A_out0: A --in=0--> A, --in=1--> B
                next_state = 'A' if in_val == 0 else 'B'
            elif state == 'B':
                # rule state_B_out0: B --in=0--> C, --in=1--> B
                next_state = 'C' if in_val == 0 else 'B'
            elif state == 'C':
                # rule state_C_out0: C --in=0--> A, --in=1--> D
                next_state = 'A' if in_val == 0 else 'D'
            elif state == 'D':
                # rule state_D_out1: D --in=0--> C, --in=1--> B
                next_state = 'C' if in_val == 0 else 'B'
            else:
                next_state = 'A'
        state = next_state
        # Moore output is determined by the state after the sampled posedge.
        # rule state_A_out0, state_B_out0, state_C_out0, state_D_out1
        out = 1 if state == 'D' else 0
        outputs.append({'out': out})
    return outputs
