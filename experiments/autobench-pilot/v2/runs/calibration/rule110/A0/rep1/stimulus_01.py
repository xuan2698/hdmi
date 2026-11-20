def stimulus(rng, cycles):
    result = []
    q = 0
    for i in range(cycles):
        load = 0
        data = 0
        if i == 0:
            load = 1
            data = rng.getrandbits(512)
        elif i < 4:
            load = 1
            data = rng.getrandbits(512)
        elif i < 8:
            load = 0
            data = 0
        else:
            r = rng.random()
            if r < 0.1:
                load = 1
                data = rng.getrandbits(512)
            elif r < 0.2:
                load = 1
                data = 0
            elif r < 0.3:
                load = 1
                data = (1 << 512) - 1
            elif r < 0.4:
                load = 1
                data = 1
            elif r < 0.5:
                load = 1
                data = 1 << 511
            elif r < 0.6:
                load = 1
                data = rng.choice([0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,
                                   0x55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555])
            else:
                load = 0
                data = 0
        result.append({'load': load, 'data': data})
    return result
