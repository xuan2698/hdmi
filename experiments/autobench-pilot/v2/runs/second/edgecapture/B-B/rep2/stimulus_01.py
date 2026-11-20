def stimulus(rng, cycles):
    result = []
    prev_in = 0
    for i in range(cycles):
        r = rng.random()
        if r < 0.08:
            reset = 1
        else:
            reset = 0
        mode = rng.randrange(6)
        if mode == 0:
            in_val = 0
        elif mode == 1:
            in_val = 0xFFFFFFFF
        elif mode == 2:
            in_val = prev_in
        elif mode == 3:
            in_val = prev_in ^ 0xFFFFFFFF
        elif mode == 4:
            in_val = rng.getrandbits(32)
        else:
            bit = rng.randrange(32)
            in_val = prev_in ^ (1 << bit)
        result.append({'reset': reset, 'in': in_val & 0xFFFFFFFF})
        prev_in = in_val & 0xFFFFFFFF
    return result
