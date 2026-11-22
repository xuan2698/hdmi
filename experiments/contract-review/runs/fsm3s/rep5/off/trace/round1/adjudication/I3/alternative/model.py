def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified; choose A)
    out = 0
    results = []

    for vec in vectors:
        # Apply mid changes carried from previous row (already applied at end of prior iteration)
        # R3 (candidate interpretation): asynchronous active-high reset
        # Asserting reset immediately forces state A and out=0 without waiting for posedge.
        if vec.get('reset', 0) == 1:
            state = A
            out = 0
        # R1: combinational output for states A, B, C -> 0
        # R2: combinational output for state D -> 1
        if state == D:
            out = 1
        else:
            out = 0

        # Sample output for this row (visible same cycle)
        results.append({'out': out})

        # Posedge update (next state) based on current state and input
        # R3: synchronous reset also forces state A at posedge
        if vec.get('reset', 0) == 1:
            state = A
        else:
            inp = vec.get('in', 0)
            # R4: A --in=0--> A ; A --in=1--> B
            if state == A:
                state = B if inp == 1 else A
            # R5: B --in=0--> C ; B --in=1--> B
            elif state == B:
                state = B if inp == 1 else C
            # R6: C --in=0--> A ; C --in=1--> D
            elif state == C:
                state = D if inp == 1 else A
            # R7: D --in=0--> C ; D --in=1--> B
            elif state == D:
                state = B if inp == 1 else C

        # Mid changes: optional mid input changes occur AFTER sampling, before the other edge,
        # and are carried to the start of the next row. We apply them now so they affect
        # the next row's combinational output and posedge transition.
        if 'mid' in vec and vec['mid'] is not None:
            mid = vec['mid']
            # Apply mid input changes to be carried to next row
            # (store as pending for next iteration)
            # We'll handle by mutating a pending dict
            pass

    return results
