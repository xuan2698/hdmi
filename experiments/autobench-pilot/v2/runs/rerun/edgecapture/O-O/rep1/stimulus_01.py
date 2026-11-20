def stimulus(rng, cycles):
    result = []
    prev_in = 0
    for i in range(cycles):
        reset = 0
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
                in_val = prev_in
            elif r < 0.35:
                in_val = prev_in & rng.getrandbits(32)
            elif r < 0.55:
                in_val = prev_in | rng.getrandbits(32)
            elif r < 0.75:
                in_val = prev_in ^ rng.getrandbits(32)
            elif r < 0.85:
                in_val = (~prev_in) & 0xFFFFFFFF
            elif r < 0.95:
                in_val = rng.choice([0, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555, 1, 0x80000000])
            else:
                in_val = rng.getrandbits(32)
        result.append({'reset': reset, 'in': in_val & 0xFFFFFFFF})
        prev_in = in_val & 0xFFFFFFFF
    return result
