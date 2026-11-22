def reference(vectors):
    # Moore FSM for Lemmings
    # States: 0=WALK_LEFT, 1=WALK_RIGHT, 2=FALL, 3=DIG, 4=SPLAT
    # Direction memory for fall/dig resume: dir 0=left, 1=right
    # Fall counter

    def decode(state):
        if state == 0:
            return {"walk_left": 1, "walk_right": 0, "aaah": 0, "digging": 0}
        elif state == 1:
            return {"walk_left": 0, "walk_right": 1, "aaah": 0, "digging": 0}
        elif state == 2:
            return {"walk_left": 0, "walk_right": 0, "aaah": 1, "digging": 0}
        elif state == 3:
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 1}
        else:
            return {"walk_left": 0, "walk_right": 0, "aaah": 0, "digging": 0}

    # Initialize state (power-up unspecified; use WALK_LEFT as default)
    state = 0
    fall_dir = 0  # direction to resume after fall/dig: 0=left, 1=right
    fall_count = 0

    results = []
    for row in vectors:
        # Apply asynchronous reset if areset is high (positive edge triggered async)
        # In this model, areset is checked before sampling; if high, reset state
        if row.get("areset", 0) == 1:
            state = 0
            fall_dir = 0
            fall_count = 0

        # Output is Moore-decoded from current state (before clock edge)
        out = decode(state)
        results.append(out)

        # Compute next state based on inputs (sampled at posedge)
        bump_left = row.get("bump_left", 0)
        bump_right = row.get("bump_right", 0)
        ground = row.get("ground", 1)
        dig = row.get("dig", 0)

        if state == 0:  # WALK_LEFT
            if ground == 0:
                state = 2
                fall_dir = 0
                fall_count = 1
            elif dig == 1:
                state = 3
                fall_dir = 0
            elif bump_left == 1 or bump_right == 1:
                state = 1
        elif state == 1:  # WALK_RIGHT
            if ground == 0:
                state = 2
                fall_dir = 1
                fall_count = 1
            elif dig == 1:
                state = 3
                fall_dir = 1
            elif bump_left == 1 or bump_right == 1:
                state = 0
        elif state == 2:  # FALL
            if ground == 1:
                if fall_count > 20:
                    state = 4
                else:
                    state = 0 if fall_dir == 0 else 1
                fall_count = 0
            else:
                fall_count += 1
        elif state == 3:  # DIG
            if ground == 0:
                state = 2
                fall_count = 1
            # else stay digging
        elif state == 4:  # SPLAT
            pass  # absorbing

    return results
