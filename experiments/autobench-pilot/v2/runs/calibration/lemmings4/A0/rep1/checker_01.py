def reference(vectors):
    # State encoding:
    # mode: 0 = walking, 1 = falling, 2 = digging, 3 = splattered
    # dir: 0 = left, 1 = right
    # fall_count: number of cycles fallen
    # Outputs are Moore: based on current state after transition.
    # areset is async positive edge: reset to walk_left (mode=0, dir=0, fall_count=0)
    # We process each sample: inputs driven before rising edge; outputs observed after edge.
    # So for each row: apply areset if 1 (async reset dominates), else compute next state from current state and inputs.
    # Initial state: unknown power-up -> None outputs? Spec says areset resets to walk left.
    # For first sample, if areset not asserted, state is unknown. We'll use None for outputs until reset.
    # But we must return list of dicts. Use None for undefined outputs.
    # Let's track state as None initially (unknown).
    state = None  # (mode, dir, fall_count)
    results = []
    for row in vectors:
        areset = row.get('areset', 0)
        bump_left = row.get('bump_left', 0)
        bump_right = row.get('bump_right', 0)
        ground = row.get('ground', 0)
        dig = row.get('dig', 0)
        
        if areset == 1:
            state = (0, 0, 0)  # walking left
        elif state is None:
            # no reset yet, state unknown
            pass
        else:
            mode, direction, fall_count = state
            if mode == 3:  # splattered
                pass  # stays splattered
            elif mode == 1:  # falling
                if ground == 1:
                    # hit ground
                    if fall_count > 20:
                        mode = 3  # splatter
                        direction = 0
                        fall_count = 0
                    else:
                        mode = 0  # resume walking same direction
                        fall_count = 0
                else:
                    fall_count += 1
            elif mode == 2:  # digging
                if ground == 0:
                    # reached other side, start falling
                    mode = 1
                    fall_count = 1  # first cycle of falling? Actually this cycle ground=0, so falling starts now.
                    # fall_count counts cycles fallen. This cycle is first fall cycle.
                # else continue digging
            elif mode == 0:  # walking
                if ground == 0:
                    # fall has precedence
                    mode = 1
                    fall_count = 1
                elif dig == 1:
                    mode = 2  # start digging
                else:
                    # check bumps
                    if bump_left == 1 and bump_right == 1:
                        direction = 1 - direction
                    elif bump_left == 1:
                        direction = 1  # walk right
                    elif bump_right == 1:
                        direction = 0  # walk left
            state = (mode, direction, fall_count)
        
        # produce outputs
        if state is None:
            out = {'walk_left': None, 'walk_right': None, 'aaah': None, 'digging': None}
        else:
            mode, direction, fall_count = state
            if mode == 0:
                out = {'walk_left': 1 if direction == 0 else 0,
                       'walk_right': 1 if direction == 1 else 0,
                       'aaah': 0, 'digging': 0}
            elif mode == 1:
                out = {'walk_left': 0, 'walk_right': 0, 'aaah': 1, 'digging': 0}
            elif mode == 2:
                out = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 1}
            else:  # splattered
                out = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        results.append(out)
    return results
