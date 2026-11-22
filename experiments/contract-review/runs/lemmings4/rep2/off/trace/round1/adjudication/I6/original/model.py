def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
        # R2, R3, R4, R5, R6: combinational outputs per state
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
    results = []

    for row in vectors:
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        # R1: asynchronous reset forces WALK_LEFT, visible same cycle
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0

        # Outputs are combinational from current state (R2-R6)
        results.append(outputs(state))

        # Compute next state on posedge
        ns = state
        nfc = fall_count

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            ns = SPLAT
            nfc = 0
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence
                ns = FALL_LEFT
                nfc = 1
            elif dig == 1:
                # R9
                ns = DIG_LEFT
                nfc = 0
            elif bump_left == 1:
                # R11 (also R13 both bumps -> switch)
                ns = WALK_RIGHT
                nfc = 0
            else:
                ns = WALK_LEFT
                nfc = 0
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8
                ns = FALL_RIGHT
                nfc = 1
            elif dig == 1:
                # R10
                ns = DIG_RIGHT
                nfc = 0
            elif bump_right == 1:
                # R12 (also R14 both bumps -> switch)
                ns = WALK_LEFT
                nfc = 0
            else:
                ns = WALK_RIGHT
                nfc = 0
        elif state == FALL_LEFT:
            if ground == 1:
                if fall_count > 20:
                    # R17
                    ns = SPLAT
                    nfc = 0
                else:
                    # R15
                    ns = WALK_LEFT
                    nfc = 0
            else:
                ns = FALL_LEFT
                nfc = fall_count + 1
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    # R17
                    ns = SPLAT
                    nfc = 0
                else:
                    # R16
                    ns = WALK_RIGHT
                    nfc = 0
            else:
                ns = FALL_RIGHT
                nfc = fall_count + 1
        elif state == DIG_LEFT:
            if ground == 0:
                # R18
                ns = FALL_LEFT
                nfc = 1
            else:
                # R19
                ns = DIG_LEFT
                nfc = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                # R18
                ns = FALL_RIGHT
                nfc = 1
            else:
                # R19
                ns = DIG_RIGHT
                nfc = 0

        state = ns
        fall_count = nfc

    return results
