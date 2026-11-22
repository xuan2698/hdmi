def reference(vectors):
    # State encoding: A=0, B=1, C=2, D=3
    # R3 (modified): reset has priority only when in=0; in=1 overrides reset.
    # Initial state: A (per candidate interpretation for global uncertainty).
    state = 0  # A

    def out_of(s):
        # R1: state A/B/C -> out 0
        # R2: state D -> out 1
        return 1 if s == 3 else 0

    results = []
    for vec in vectors:
        inp = vec.get('in', 0)
        rst = vec.get('reset', 0)

        # Combinational output visible same cycle (R1, R2)
        results.append({'out': out_of(state)})

        # Compute next state at posedge
        # R3 (modified): reset active high, but in=1 overrides reset
        if rst == 1 and inp == 0:
            state = 0  # A
        else:
            if state == 0:  # A
                # R4
                state = 1 if inp == 1 else 0
            elif state == 1:  # B
                # R5
                state = 1 if inp == 1 else 2
            elif state == 2:  # C
                # R6
                state = 3 if inp == 1 else 0
            else:  # D
                # R7
                state = 1 if inp == 1 else 2

    return results
