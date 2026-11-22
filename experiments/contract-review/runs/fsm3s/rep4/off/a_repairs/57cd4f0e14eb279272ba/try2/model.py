def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R1-R4: Moore outputs are combinational from current state (same_cycle)
    # R5: synchronous active high reset forces state A on posedge
    # R6-R9: next-state transitions on posedge
    # Mid changes occur AFTER sampling, before other edge, carried to next row.
    # We sample at posedge: output reflects state BEFORE the edge (current state),
    # then state updates for next cycle.

    state = 0  # power-up unspecified; start at A (reset default)

    def out_of(s):
        # R1: state A -> out 0
        # R2: state B -> out 0
        # R3: state C -> out 0
        # R4: state D -> out 1
        return 1 if s == 3 else 0

    results = []
    for row in vectors:
        inp = row.get("in", 0)
        rst = row.get("reset", 0)

        # Output is combinational from current state (same_cycle) - R1..R4
        results.append({"out": out_of(state)})

        # Compute next state on posedge
        if rst == 1:
            # R5: synchronous active high reset -> state A
            state = 0
        else:
            # R6-R9: explicit transitions
            if state == 0:      # A
                state = 1 if inp == 1 else 0   # R6
            elif state == 1:    # B
                state = 1 if inp == 1 else 2   # R7
            elif state == 2:    # C
                state = 3 if inp == 1 else 0   # R8
            elif state == 3:    # D
                state = 1 if inp == 1 else 2   # R9

    return results
