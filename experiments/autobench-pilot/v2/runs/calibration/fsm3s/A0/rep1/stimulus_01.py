def stimulus(rng, cycles):
    result = []
    state = 'A'
    for i in range(cycles):
        r = rng.random()
        if i == 0:
            reset = 1
            inp = 0
        elif r < 0.1:
            reset = 1
            inp = rng.getrandbits(1)
        else:
            reset = 0
            inp = rng.getrandbits(1)
        result.append({'in': inp, 'reset': reset})
    return result
