def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    # Output per state (Moore)
    OUT = {A: 0, B: 0, C: 0, D: 1}
    # Next state table: NEXT[state][in]
    NEXT = {
        A: {0: A, 1: B},
        B: {0: C, 1: B},
        C: {0: A, 1: D},
        D: {0: C, 1: B},
    }

    # Power-on: initialize to state A (candidate interpretation for global)
    state = A
    results = []

    for row in vectors:
        # R_RESET: synchronous active high reset -> next state A, output 0
        # R_TRANS: next state determined by table on posedge when reset == 0
        # Sampling occurs at posedge; mid changes are applied after sampling.
        # We compute the output for the current (pre-edge) state first (Moore,
        # combinational, same_cycle), then update state for next cycle.
        # R_A / R_B / R_C / R_D: combinational output based on current state
        out_val = OUT[state]
        results.append({"out": out_val & 0x1})

        # Compute next state at posedge
        if row.get("reset", 0) == 1:
            # R_RESET
            state = A
        else:
            # R_TRANS
            in_val = row.get("in", 0) & 0x1
            state = NEXT[state][in_val]

    return results
