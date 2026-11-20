def stimulus(rng, cycles):
    result = []
    prev_in = 0
    for i in range(cycles):
        # Determine reset: active high synchronous
        # Vary reset patterns: mostly low, occasional high
        if i == 0:
            reset = 1
        elif i < 3:
            reset = rng.choice([0, 1])
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
            else:
                reset = 0

        # Generate input with targeted transitions
        if i == 0:
            in_val = rng.getrandbits(32)
        else:
            mode = rng.randrange(10)
            if mode < 3:
                # Random full value
                in_val = rng.getrandbits(32)
            elif mode < 5:
                # Clear some bits (1->0 transitions)
                in_val = prev_in & rng.getrandbits(32)
            elif mode < 7:
                # Set some bits (0->1 transitions)
                in_val = prev_in | rng.getrandbits(32)
            elif mode < 8:
                # Toggle bits
                in_val = prev_in ^ rng.getrandbits(32)
            elif mode < 9:
                # All zeros
                in_val = 0
            else:
                # All ones
                in_val = 0xFFFFFFFF

        in_val &= 0xFFFFFFFF
        result.append({'reset': reset, 'in': in_val})
        prev_in = in_val
    return result
