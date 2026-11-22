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
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0
            result.append(outputs(state))
            continue

        # Combinational output for current state (sampled before edge)
        result.append(outputs(state))

        # Compute next state at posedge
        ns = state
        nfc = fall_count

        if state == SPLAT:
            # R20: SPLAT stays SPLAT
            ns = SPLAT
            nfc = 0
        elif state == WALK_LEFT:
            if ground == 0:
                # R7: fall precedence; R22: bump ignored on ground-disappear cycle
                ns = FALL_LEFT
                nfc = 1  # R17 interp: ground=0 cycle counts as fall cycle 1
            elif dig == 1:
                # R9: dig
                ns = DIG_LEFT
                nfc = 0
            elif bump_left == 1:
                # R11, R13: bump left (or both) -> walk right
                ns = WALK_RIGHT
                nfc = 0
            else:
                ns = WALK_LEFT
                nfc = 0
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8: fall; R22: bump ignored
                ns = FALL_RIGHT
                nfc = 1
            elif dig == 1:
                # R10: dig
                ns = DIG_RIGHT
                nfc = 0
            elif bump_right == 1:
                # R12, R14: bump right (or both) -> walk left
                ns = WALK_LEFT
                nfc = 0
            else:
                ns = WALK_RIGHT
                nfc = 0
        elif state == FALL_LEFT:
            if ground == 1:
                # R15/R17: land; check fall_count
                if fall_count > 20:
                    ns = SPLAT
                else:
                    ns = WALK_LEFT
                nfc = 0
            else:
                # R21: bump ignored while falling; R24: dig ignored
                ns = FALL_LEFT
                nfc = fall_count + 1
        elif state == FALL_RIGHT:
            if ground == 1:
                if fall_count > 20:
                    ns = SPLAT
                else:
                    ns = WALK_RIGHT
                nfc = 0
            else:
                ns = FALL_RIGHT
                nfc = fall_count + 1
        elif state == DIG_LEFT:
            if ground == 0:
                # R18: dig reaches edge -> fall
                ns = FALL_LEFT
                nfc = 1
            else:
                # R19, R24: keep digging, bump ignored
                ns = DIG_LEFT
                nfc = 0
        elif state == DIG_RIGHT:
            if ground == 0:
                ns = FALL_RIGHT
                nfc = 1
            else:
                ns = DIG_RIGHT
                nfc = 0

        state = ns
        fall_count = nfc

    return result
