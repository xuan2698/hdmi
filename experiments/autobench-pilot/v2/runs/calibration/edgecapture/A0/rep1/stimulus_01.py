def stimulus(rng, cycles):
    result = []
    prev_in = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            in_val = rng.getrandbits(32)
        elif i == 1:
            reset = 0
            in_val = rng.getrandbits(32)
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
                in_val = rng.getrandbits(32)
            elif r < 0.15:
                reset = 0
                in_val = prev_in
            elif r < 0.35:
                reset = 0
                in_val = prev_in & rng.getrandbits(32)
            elif r < 0.55:
                reset = 0
                in_val = prev_in | rng.getrandbits(32)
            elif r < 0.65:
                reset = 0
                in_val = (~prev_in) & 0xFFFFFFFF
            elif r < 0.75:
                reset = 0
                in_val = 0
            elif r < 0.85:
                reset = 0
                in_val = 0xFFFFFFFF
            else:
                reset = 0
                in_val = rng.getrandbits(32)
        result.append({'reset': reset, 'in': in_val})
        prev_in = in_val
    return result
