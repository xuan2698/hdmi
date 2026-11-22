def reference(vectors):
    # State encoding
    WALK_LEFT, WALK_RIGHT, FALL_LEFT, FALL_RIGHT, DIG_LEFT, DIG_RIGHT, SPLAT = range(7)

    def outputs(state):
        # R2, R3, R4, R5, R6: combinational outputs from state
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
        areset = row.get("areset", 0)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 0)
        dig = row.get("dig", 0)

        # R1: asynchronous reset forces WALK_LEFT, visible same cycle
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Outputs are combinational from current state (R2-R6)
        result.append(outputs(state))

        # Compute next state on posedge
        ns = state
        nfc = fall_count

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            ns = SPLAT
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence
                ns = FALL_LEFT
                nfc = 1
            elif dig == 1:
                # R9: start digging
                ns = DIG_LEFT
            elif bump_left == 1:
                # R11, R13: bump left (or both) -> walk right
                ns = WALK_RIGHT
            else:
                ns = WALK_LEFT
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8
                ns = FALL_RIGHT
                nfc = 1
            elif dig == 1:
                # R10
                ns = DIG_RIGHT
            elif bump_right == 1:
                # R12, R14: bump right (or both) -> walk left
                ns = WALK_LEFT
            else:
                ns = WALK_RIGHT
        elif state == FALL_LEFT:
            if ground == 1:
                # R17: splat if fall_count > 20
                if fall_count > 20:
                    ns = SPLAT
                else:
                    # R15: resume walking left
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
                else:
                    # R16
                    ns = WALK_RIGHT
                nfc = 0
            else:
                ns = FALL_RIGHT
                nfc = fall_count + 1
        elif state == DIG_LEFT:
            if ground == 0:
                # R18: fall
                ns = FALL_LEFT
                nfc = 1
            else:
                # R19: continue digging (ignore dig input)
                ns = DIG_LEFT
        elif state == DIG_RIGHT:
            if ground == 0:
                # R18
                ns = FALL_RIGHT
                nfc = 1
            else:
                # R19
                ns = DIG_RIGHT

        state = ns
        fall_count = nfc

    return result
