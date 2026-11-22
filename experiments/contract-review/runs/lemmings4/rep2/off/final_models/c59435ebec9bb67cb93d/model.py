def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
        # R2, R3, R4, R5, R6: combinational outputs by state
        if state == WALK_LEFT:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        if state == WALK_RIGHT:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        if state in (FALL_LEFT, FALL_RIGHT):
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        if state in (DIG_LEFT, DIG_RIGHT):
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        # SPLAT
        return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    state = WALK_LEFT
    fall_count = 0
    result = []

    for row in vectors:
        areset = row["areset"]
        bump_left = row["bump_left"]
        bump_right = row["bump_right"]
        ground = row["ground"]
        dig = row["dig"]

        # R1: asynchronous reset forces WALK_LEFT, visible same cycle
        if areset:
            state = WALK_LEFT
            fall_count = 0

        # Outputs are combinational from current state (same cycle)
        result.append(outputs(state))

        # Compute next state at posedge
        if areset:
            # reset holds state at WALK_LEFT
            state = WALK_LEFT
            fall_count = 0
            continue

        ns = state
        nfc = fall_count

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            ns = SPLAT
            nfc = 0
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence; R22 bump ignored on ground-disappear
                ns = FALL_LEFT
                nfc = 0
            elif dig == 1:
                # R9: start digging
                ns = DIG_LEFT
                nfc = 0
            else:
                # R11, R13: bump_left (or both) -> WALK_RIGHT
                if bump_left == 1:
                    ns = WALK_RIGHT
                else:
                    ns = WALK_LEFT
                nfc = 0
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8: fall; R22 bump ignored
                ns = FALL_RIGHT
                nfc = 0
            elif dig == 1:
                # R10: start digging
                ns = DIG_RIGHT
                nfc = 0
            else:
                # R12, R14: bump_right (or both) -> WALK_LEFT
                if bump_right == 1:
                    ns = WALK_LEFT
                else:
                    ns = WALK_RIGHT
                nfc = 0
        elif state in (FALL_LEFT, FALL_RIGHT):
            if ground == 1:
                # R15/R16/R17/R23: land; bump ignored
                if fall_count > 20:
                    ns = SPLAT
                else:
                    ns = WALK_LEFT if state == FALL_LEFT else WALK_RIGHT
                nfc = 0
            else:
                # R21: still falling, bump ignored, dig ignored
                ns = state
                nfc = fall_count + 1
        elif state in (DIG_LEFT, DIG_RIGHT):
            if ground == 0:
                # R18: fall in remembered direction
                ns = FALL_LEFT if state == DIG_LEFT else FALL_RIGHT
                nfc = 0
            else:
                # R19, R24: keep digging, bump ignored
                ns = state
                nfc = 0

        state = ns
        fall_count = nfc

    return result
