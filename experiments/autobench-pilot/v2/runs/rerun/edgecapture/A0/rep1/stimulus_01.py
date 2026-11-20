def stimulus(rng, cycles):
    result = []
    prev_in = 0
    for i in range(cycles):
        # Occasionally assert reset
        if i == 0:
            reset = 1
            in_val = rng.getrandbits(32)
        elif rng.random() < 0.1:
            reset = 1
            in_val = rng.getrandbits(32)
        else:
            reset = 0
            r = rng.random()
            if r < 0.25:
                # All ones
                in_val = 0xFFFFFFFF
            elif r < 0.5:
                # All zeros
                in_val = 0
            elif r < 0.65:
                # Toggle all bits from previous
                in_val = (~prev_in) & 0xFFFFFFFF
            elif r < 0.8:
                # Single bit flip
                bit = rng.randrange(32)
                in_val = prev_in ^ (1 << bit)
            elif r < 0.9:
                # Single bit set
                bit = rng.randrange(32)
                in_val = 1 << bit
            else:
                in_val = rng.getrandbits(32)
        result.append({'reset': reset, 'in': in_val})
        prev_in = in_val
    return result
