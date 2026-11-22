def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R1-R4: Moore outputs are combinational from current state (visible same cycle)
    # R5: synchronous active-high reset forces state A at posedge
    # R6-R9: next-state transitions at posedge
    state = 0  # power-up unspecified; start at A
    out = []
    for vec in vectors:
        # R1-R4: output depends on current state (combinational, same cycle)
        if state == 0:      # R1: state A -> out 0
            o = 0
        elif state == 1:    # R2: state B -> out 0
            o = 0
        elif state == 2:    # R3: state C -> out 0
            o = 0
        else:               # R4: state D -> out 1
            o = 1
        out.append({"out": o})
        # R5: synchronous active-high reset -> state A at posedge
        if vec["reset"] == 1:
            state = 0
        else:
            # R6-R9: next-state transitions at posedge
            if state == 0:      # R6
                state = 1 if vec["in"] == 1 else 0
            elif state == 1:    # R7
                state = 1 if vec["in"] == 1 else 2
            elif state == 2:    # R8
                state = 3 if vec["in"] == 1 else 0
            else:               # R9
                state = 1 if vec["in"] == 1 else 2
    return out
