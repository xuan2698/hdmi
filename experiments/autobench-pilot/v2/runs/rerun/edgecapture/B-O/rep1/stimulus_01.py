def stimulus(rng, cycles):
    result = []
    prev_in = 0
    for i in range(cycles):
        reset = 0
        if i == 0:
            reset = 1
        elif rng.random() < 0.05:
            reset = 1
        if rng.random() < 0.3:
            in_val = rng.getrandbits(32)
        elif rng.random() < 0.5:
            in_val = prev_in ^ (1 << rng.randrange(32))
        elif rng.random() < 0.5:
            in_val = prev_in & ~(1 << rng.randrange(32))
        else:
            in_val = prev_in
        if rng.random() < 0.1:
            in_val = 0
        elif rng.random() < 0.1:
            in_val = 0xFFFFFFFF
        result.append({'reset': reset, 'in': in_val & 0xFFFFFFFF})
        prev_in = in_val & 0xFFFFFFFF
    return result
