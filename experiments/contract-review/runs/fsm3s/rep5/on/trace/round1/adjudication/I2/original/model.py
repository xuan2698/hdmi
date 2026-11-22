def reference(vectors):
    state = 'A'  # power-up assumed A for concrete unsigned output
    result = []
    for row in vectors:
        reset = row.get('reset', 0)
        in_val = row.get('in', 0)
        # synchronous active high reset
        if reset:
            state = 'A'
        else:
            # explicit state transitions
            if state == 'A':
                state = 'A' if in_val == 0 else 'B'
            elif state == 'B':
                state = 'C' if in_val == 0 else 'B'
            elif state == 'C':
                state = 'A' if in_val == 0 else 'D'
            elif state == 'D':
                state = 'C' if in_val == 0 else 'B'
        # Moore output based on updated state
        if state == 'A':
            out = 0  # out_A
        elif state == 'B':
            out = 0  # out_B
        elif state == 'C':
            out = 0  # out_C
        else:  # state == 'D'
            out = 1  # out_D
        result.append({'out': out})
    return result
