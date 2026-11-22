def reference(vectors):
    # Moore FSM for Lemmings.
    # States:
    #   WL  = walk left
    #   WR  = walk right
    #   FL  = falling, remembered direction left
    #   FR  = falling, remembered direction right
    #   DL  = digging, remembered direction left
    #   DR  = digging, remembered direction right
    #   SPL = splattered
    #
    # Outputs (Moore):
    #   WL: walk_left=1
    #   WR: walk_right=1
    #   FL/FR: aaah=1
    #   DL/DR: digging=1
    #   SPL: all 0
    #
    # Fall counter: counts cycles spent falling. Splatter if fall duration > 20
    # when landing (ground=1 while falling).
    #
    # Timing: areset is async positive-edge. Each row's inputs are driven before
    # the sampled posedge. Mid changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.
    #
    # We model: for each row, apply async reset if areset==1 (takes effect
    # immediately, before the posedge). Then sample at posedge using the row's
    # input values (which are the values at the posedge, since mid changes happen
    # after sampling). Then apply mid changes (which affect the next row's start
    # state, but since next row's inputs are driven before its posedge, mid
    # changes only matter if they change state via async reset — but areset mid
    # change could reset asynchronously).
    #
    # Actually the protocol: "Each row's values are driven before the sampled edge.
    # Optional mid input changes occur AFTER sampling, before the other edge, and
    # are carried to the start of the next row."
    #
    # So per row: inputs are the values at the posedge. Mid changes happen after
    # the posedge, before the next posedge, and their effect is that the next row
    # starts with those mid values (which are then possibly overridden by the next
    # row's driven values before its posedge). Since the next row's driven values
    # are applied before its posedge, mid changes only matter for async reset
    # (areset) which is level-sensitive: if areset goes high mid-cycle, it resets
    # immediately.
    #
    # We'll handle: at start of row, state is whatever it was. Apply async reset
    # if areset==1 (from row's driven value OR carried mid value). Then posedge
    # samples with row's inputs. Then mid changes: if areset mid goes high, reset
    # state asynchronously (affects next row start). Other mid changes don't
    # affect state until next posedge, and next row's driven values override them
    # anyway (since driven before posedge). So only areset mid matters.

    # State encoding
    WL, WR, FL, FR, DL, DR, SPL = range(7)

    state = WL
    fall_count = 0

    results = []

    for row in vectors:
        # Row may contain 'mid' dict for mid-cycle changes
        # Extract inputs
        areset = row.get('areset', 0)
        bump_left = row.get('bump_left', 0)
        bump_right = row.get('bump_right', 0)
        ground = row.get('ground', 1)
        dig = row.get('dig', 0)

        # Apply async reset if areset is high (driven before posedge)
        if areset:
            state = WL
            fall_count = 0

        # Sample at posedge: compute next state from current state and inputs
        # Precedence: fall (ground=0) > dig > direction switch
        if state == SPL:
            next_state = SPL
            next_fall = 0
        elif state in (FL, FR):
            # Falling
            if ground == 0:
                # Continue falling, increment counter
                next_state = state
                next_fall = fall_count + 1
            else:
                # Landing
                if fall_count > 20:
                    next_state = SPL
                    next_fall = 0
                else:
                    # Resume walking in remembered direction
                    next_state = WL if state == FL else WR
                    next_fall = 0
        elif state in (DL, DR):
            # Digging
            if ground == 0:
                # Fall, remember direction
                next_state = FL if state == DL else FR
                next_fall = 1  # first cycle of falling
            else:
                # Continue digging
                next_state = state
                next_fall = 0
        elif state in (WL, WR):
            # Walking
            if ground == 0:
                # Fall, remember direction
                next_state = FL if state == WL else FR
                next_fall = 1
            elif dig == 1:
                # Start digging
                next_state = DL if state == WL else DR
                next_fall = 0
            else:
                # Check bumps
                bumped = bump_left or bump_right
                if bumped:
                    # Switch direction
                    next_state = WR if state == WL else WL
                else:
                    next_state = state
                next_fall = 0
        else:
            next_state = state
            next_fall = fall_count

        state = next_state
        fall_count = next_fall

        # Compute outputs (Moore)
        out = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if state == WL:
            out['walk_left'] = 1
        elif state == WR:
            out['walk_right'] = 1
        elif state in (FL, FR):
            out['aaah'] = 1
        elif state in (DL, DR):
            out['digging'] = 1
        # SPL: all 0

        results.append(out)

        # Apply mid changes: only areset matters (async reset)
        mid = row.get('mid', {})
        if mid.get('areset', 0):
            state = WL
            fall_count = 0

    return results
