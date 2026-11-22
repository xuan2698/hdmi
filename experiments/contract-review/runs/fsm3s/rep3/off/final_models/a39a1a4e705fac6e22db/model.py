def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    A, B, C, D = 0, 1, 2, 3

    # Output per state (Moore): A->0, B->0, C->0, D->1
    # R1: states A,B,C output 0 (combinational, same_cycle)
    # R2: state D output 1 (combinational, same_cycle)
    def out_of(state):
        # R1, R2
        return 1 if state == D else 0

    # Initial state: contract candidate says initial state is A even before first reset release.
    state = A

    results = []
    for vec in vectors:
        inp = vec.get("in", 0) & 1
        rst = vec.get("reset", 0) & 1

        # Sample: compute output from current state (combinational, same_cycle)
        # R1, R2
        out = out_of(state)

        # R3: synchronous active high reset -> next state A, output follows state A (out=0)
        # R4-R7: next-state logic when reset==0
        if rst == 1:
            # R3: reset forces state A; output during reset follows state A (out=0)
            next_state = A
            out = 0  # R3 interpretation: output during reset follows state A
        else:
            # R4: A -> in==0: A, in==1: B
            # R5: B -> in==0: C, in==1: B
            # R6: C -> in==0: A, in==1: D
            # R7: D -> in==0: C, in==1: B
            if state == A:
                next_state = B if inp == 1 else A  # R4
            elif state == B:
                next_state = B if inp == 1 else C  # R5
            elif state == C:
                next_state = D if inp == 1 else A  # R6
            else:  # state == D
                next_state = B if inp == 1 else C  # R7

        results.append({"out": out & 1})

        # Update state at posedge (after sampling)
        state = next_state

    return results
