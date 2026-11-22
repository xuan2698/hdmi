def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R1-R4: Moore outputs are combinational from current state (same_cycle visible)
    # R5: synchronous active high reset forces state A on posedge
    # R6-R9: next-state transitions on posedge
    # Mid input changes occur AFTER sampling, before the other edge, carried to next row.
    state = 0  # power-up unspecified; start at A
    out_vals = []
    for vec in vectors:
        # R1-R4: output depends on current state (combinational, same cycle)
        if state == 0:      # R1: state A -> out 0
            out = 0
        elif state == 1:    # R2: state B -> out 0
            out = 0
        elif state == 2:    # R3: state C -> out 0
            out = 0
        else:               # R4: state D -> out 1
            out = 1
        out_vals.append({"out": out})
        # Sample inputs at posedge
        inp = vec.get("in", 0)
        rst = vec.get("reset", 0)
        # R5: synchronous active high reset -> state A
        if rst == 1:
            state = 0
        else:
            # R6-R9: explicit transitions
            if state == 0:      # R6
                state = 0 if inp == 0 else 1
            elif state == 1:    # R7
                state = 2 if inp == 0 else 1
            elif state == 2:    # R8
                state = 0 if inp == 0 else 3
            else:               # R9
                state = 2 if inp == 0 else 1
    return out_vals
