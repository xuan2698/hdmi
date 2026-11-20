def stimulus(rng, cycles):
    result = []
    prev_in = rng.getrandbits(32)
    for i in range(cycles):
        reset = 0
        if i == 0:
            reset = 1
            in_val = rng.getrandbits(32)
        elif i == 1:
            reset = 0
            in_val = rng.getrandbits(32)
        elif i == 2:
            reset = 0
            in_val = 0
        elif i == 3:
            reset = 0
            in_val = 0xFFFFFFFF
        elif i == 4:
            reset = 0
            in_val = 0
        elif i == 5:
            reset = 1
            in_val = 0xFFFFFFFF
        elif i == 6:
            reset = 0
            in_val = 0
        elif i == 7:
            reset = 0
            in_val = 0xFFFFFFFF
        elif i == 8:
            reset = 0
            in_val = 0xAAAAAAAA
        elif i == 9:
            reset = 0
            in_val = 0x55555555
        elif i == 10:
            reset = 0
            in_val = 0xAAAAAAAA
        elif i == 11:
            reset = 0
            in_val = 0x55555555
        elif i == 12:
            reset = 1
            in_val = 0xAAAAAAAA
        elif i == 13:
            reset = 0
            in_val = 0x55555555
        elif i == 14:
            reset = 0
            in_val = 0xAAAAAAAA
        elif i == 15:
            reset = 0
            in_val = 0x55555555
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
            elif r < 0.15:
                in_val = prev_in
            elif r < 0.25:
                in_val = (~prev_in) & 0xFFFFFFFF
            elif r < 0.35:
                in_val = 0
            elif r < 0.45:
                in_val = 0xFFFFFFFF
            elif r < 0.55:
                in_val = prev_in ^ rng.getrandbits(32)
            elif r < 0.65:
                in_val = prev_in & rng.getrandbits(32)
            elif r < 0.75:
                in_val = prev_in | rng.getrandbits(32)
            else:
                in_val = rng.getrandbits(32)
        prev_in = in_val
        result.append({'reset': reset, 'in': in_val})
    return result
