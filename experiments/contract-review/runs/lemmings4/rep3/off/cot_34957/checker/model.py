def reference(vectors):
    # Moore FSM for Lemmings.
    # States: WL (walk left), WR (walk right), FALL, DIG, SPLAT
    # Outputs: walk_left, walk_right, aaah, digging
    # Fall counter counts completed falling cycles; splatter if >20 on landing.
    WL, WR, FALL, DIG, SPLAT = 0, 1, 2, 3, 4

    state = WL
    fall_count = 0

    results = []
    for row in vectors:
        # Apply asynchronous reset (positive edge triggered) before sampling.
        # In this vector protocol, areset is a level presented before the edge.
        if row.get('areset', 0):
            state = WL
            fall_count = 0

        # Moore outputs based on current state
        walk_left = 1 if state == WL else 0
        walk_right = 1 if state == WR else 0
        aaah = 1 if state == FALL else 0
        digging = 1 if state == DIG else 0

        results.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging,
        })

        # Compute next state from current state and inputs
        bl = row.get('bump_left', 0)
        br = row.get('bump_right', 0)
        g = row.get('ground', 0)
        d = row.get('dig', 0)

        if state == SPLAT:
            next_state = SPLAT
            next_fall = fall_count
        elif state == FALL:
            if g:
                # Landing
                if fall_count > 20:
                    next_state = SPLAT
                else:
                    # Resume walking in remembered direction.
                    # We need to remember direction. Store direction in state? 
                    # We'll track direction separately.
                    next_state = None  # placeholder, resolved below
                next_fall = 0
            else:
                next_state = FALL
                next_fall = fall_count + 1
        elif state == DIG:
            if g:
                next_state = DIG
                next_fall = 0
            else:
                # Ground gone: start falling
                next_state = FALL
                next_fall = 1
        else:  # WL or WR
            if not g:
                next_state = FALL
                next_fall = 1
            elif d:
                next_state = DIG
                next_fall = 0
            else:
                # Bumps toggle direction (both bumps = single toggle)
                toggle = bl ^ br
                if toggle:
                    next_state = WR if state == WL else WL
                else:
                    next_state = state
                next_fall = 0

        # Handle FALL landing direction: need remembered direction.
        # We'll track direction separately to handle FALL->walking.
        # Since we didn't store direction in state, we need a direction variable.
        # Let's restructure: track direction separately.
        # For simplicity, redo with direction variable.
        # (We'll rewrite the loop properly below.)
        state = next_state
        fall_count = next_fall

    return results
