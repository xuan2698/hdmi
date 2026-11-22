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
        areset = row["areset"]
        bump_left = row["bump_left"]
        bump_right = row["bump_right"]
        ground = row["ground"]
        dig = row["dig"]

        # R1: asynchronous reset forces WALK_LEFT (visible same cycle)
        if areset == 1:
            state = WALK_LEFT
            fall_count = 0

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
                nfc = 0
            elif dig == 1:
                # R9: start digging
                ns = DIG_LEFT
            elif bump_left == 1 or bump_right == 1:
                # R11, R13: switch direction
                ns = WALK_RIGHT
        elif state == WALK_RIGHT:
            if ground == 0:
                # R8
                ns = FALL_RIGHT
                nfc = 0
            elif dig == 1:
                # R10
                ns = DIG_RIGHT
            elif bump_left == 1 or bump_right == 1:
                # R12, R14
                ns = WALK_LEFT
        elif state == FALL_LEFT:
            if ground == 1:
                # R15/R17: check fall duration
                # fall_count counts cycles already spent in FALL state
                # A fall of exactly 20 cycles does not splatter; 21 does.
                # When we enter FALL, nfc=0. Each subsequent cycle in FALL increments.
                # The cycle where ground=1 is detected: total fall cycles = fall_count + 1?
                # Let's reason: entering FALL at cycle T (nfc=0). At cycle T+1, if still
                # falling, nfc becomes 1. So after k cycles in FALL state (including the
                # entry cycle), fall_count = k-1. When ground=1 detected at some cycle,
                # the number of cycles spent falling = fall_count + 1.
                total_fall = fall_count + 1
                if total_fall > 20:
                    ns = SPLAT
                else:
                    ns = WALK_LEFT
                nfc = 0
            else:
                nfc = fall_count + 1
        elif state == FALL_RIGHT:
            if ground == 1:
                total_fall = fall_count + 1
                if total_fall > 20:
                    ns = SPLAT
                else:
                    ns = WALK_RIGHT
                nfc = 0
            else:
                nfc = fall_count + 1
        elif state == DIG_LEFT:
            if ground == 0:
                # R18
                ns = FALL_LEFT
                nfc = 0
            # R19: stays digging
        elif state == DIG_RIGHT:
            if ground == 0:
                ns = FALL_RIGHT
                nfc = 0

        state = ns
        fall_count = nfc

    return result
