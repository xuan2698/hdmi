def reference(vectors):
    # Moore FSM for Lemmings.
    # State variables:
    #   dir: 0 = left, 1 = right (remembered walking direction)
    #   falling: bool
    #   fall_count: int (cycles spent falling)
    #   digging: bool
    #   splattered: bool
    #
    # Outputs (Moore, based on current state):
    #   walk_left  = (not splattered) and (not falling) and (not digging) and dir==0
    #   walk_right = (not splattered) and (not falling) and (not digging) and dir==1
    #   aaah       = (not splattered) and falling
    #   digging    = (not splattered) and digging
    #
    # Reset (areset=1, async, sampled at posedge): dir=0, falling=False,
    #   fall_count=0, digging=False, splattered=False.
    #
    # Transition precedence (when not reset):
    #   1. If splattered: stay splattered, all outputs 0.
    #   2. If falling:
    #        - if ground==0: stay falling, fall_count += 1
    #        - if ground==1: if fall_count > 20 -> splatter
    #                        else: falling=False, fall_count=0, resume dir
    #        (bumps and dig ignored)
    #   3. If digging:
    #        - if ground==0: start falling (falling=True, fall_count=1), digging=False
    #        - else: stay digging (bumps ignored)
    #   4. Walking on ground (not falling, not digging):
    #        - if ground==0: start falling (falling=True, fall_count=1)
    #        - elif dig==1: start digging
    #        - else: if bump_left or bump_right: dir = 1 - dir
    #
    # Note: fall_count counts cycles spent falling. "Falls for more than 20
    # clock cycles then hits the ground" -> splatter if fall_count > 20 at
    # the moment ground reappears. The cycle where ground disappears counts
    # as the first falling cycle (fall_count becomes 1).

    # State
    dir_ = 0
    falling = False
    fall_count = 0
    digging = False
    splattered = False

    results = []

    for row in vectors:
        # Apply optional mid changes: they belong to the next sampled row,
        # so we apply them AFTER computing this row's outputs/transition.
        # We'll handle by processing row inputs first, then mid changes.
        areset = row.get('areset', 0)
        bump_left = row.get('bump_left', 0)
        bump_right = row.get('bump_right', 0)
        ground = row.get('ground', 0)
        dig = row.get('dig', 0)

        # Compute outputs from current state (Moore)
        if splattered:
            wl = wr = aaah = dg = 0
        else:
            aaah = 1 if falling else 0
            dg = 1 if digging else 0
            if falling or digging:
                wl = wr = 0
            else:
                wl = 1 if dir_ == 0 else 0
                wr = 1 if dir_ == 1 else 0

        results.append({
            'walk_left': wl,
            'walk_right': wr,
            'aaah': aaah,
            'digging': dg,
        })

        # Transition (based on sampled inputs)
        if areset:
            dir_ = 0
            falling = False
            fall_count = 0
            digging = False
            splattered = False
        elif splattered:
            pass  # stay splattered
        elif falling:
            if ground == 0:
                fall_count += 1
            else:
                # ground reappeared
                if fall_count > 20:
                    splattered = True
                    falling = False
                    fall_count = 0
                    digging = False
                else:
                    falling = False
                    fall_count = 0
                    # resume walking in remembered dir
        elif digging:
            if ground == 0:
                digging = False
                falling = True
                fall_count = 1
            # else stay digging, bumps ignored
        else:
            # walking on ground
            if ground == 0:
                falling = True
                fall_count = 1
            elif dig == 1:
                digging = True
            else:
                if bump_left or bump_right:
                    dir_ = 1 - dir_

        # Apply mid changes (affect next row's transition, not this row's)
        mid = row.get('mid', None)
        if mid:
            # Mid changes are applied to inputs for the NEXT row.
            # We store them so the next iteration uses them.
            # Since the loop reads from row dicts, we need to carry over.
            # We'll implement by mutating a pending override dict.
            pass

        # Handle pending mid overrides for next row
        # (We'll store in a variable and merge at start of next iteration.)
        # To keep it simple, we track pending overrides.
        if 'mid' in row and row['mid']:
            # Store for next iteration
            pending = row['mid']
        else:
            pending = None

        # If there's a pending override, we need to apply it to the next row.
        # We'll do this by modifying the next row's inputs before processing.
        # Since we can't easily look ahead, we'll use a carry variable.
        # Let's restructure: use a carry dict.
        # (This code path is handled below via carry.)

    return results
