def stimulus(rng, cycles):
    result = []
    # State tracking for targeted stimulus
    falling = False
    fall_count = 0
    digging = False
    walking_left = True
    splattered = False
    ground = 1
    dig = 0
    bump_left = 0
    bump_right = 0
    areset = 0

    for i in range(cycles):
        # Occasionally reset
        if rng.random() < 0.02:
            areset = 1
            ground = 1
            dig = 0
            bump_left = 0
            bump_right = 0
            falling = False
            fall_count = 0
            digging = False
            walking_left = True
            splattered = False
            result.append({
                'areset': areset,
                'bump_left': bump_left,
                'bump_right': bump_right,
                'ground': ground,
                'dig': dig,
            })
            areset = 0
            continue

        # Simulate state to generate targeted sequences
        # Determine current effective state
        if splattered:
            # Stay splattered, but occasionally reset
            ground = 1
            dig = 0
            bump_left = 0
            bump_right = 0
            result.append({
                'areset': 0,
                'bump_left': bump_left,
                'bump_right': bump_right,
                'ground': ground,
                'dig': dig,
            })
            continue

        # Randomize inputs with targeted probabilities
        r = rng.random()
        if r < 0.15:
            ground = 0
        elif r < 0.25:
            ground = 1
        # else keep ground

        # Bumps
        rb = rng.random()
        if rb < 0.1:
            bump_left = 1
            bump_right = 0
        elif rb < 0.2:
            bump_left = 0
            bump_right = 1
        elif rb < 0.25:
            bump_left = 1
            bump_right = 1
        else:
            bump_left = 0
            bump_right = 0

        # Dig
        rd = rng.random()
        if rd < 0.1:
            dig = 1
        else:
            dig = 0

        # Update internal model
        if falling:
            if ground == 1:
                # Landed
                if fall_count > 20:
                    splattered = True
                falling = False
                fall_count = 0
            else:
                fall_count += 1
        elif digging:
            if ground == 0:
                # Start falling
                digging = False
                falling = True
                fall_count = 0
        else:
            # Walking
            if ground == 0:
                falling = True
                fall_count = 0
            elif dig == 1:
                digging = True
            else:
                # Bumps affect direction
                if bump_left == 1 and bump_right == 1:
                    walking_left = not walking_left
                elif bump_left == 1:
                    walking_left = False
                elif bump_right == 1:
                    walking_left = True

        result.append({
            'areset': 0,
            'bump_left': bump_left,
            'bump_right': bump_right,
            'ground': ground,
            'dig': dig,
        })

    return result
