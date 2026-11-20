def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < 5:
            y = states[i]
            x = rng.getrandbits(1)
        elif i < 10:
            y = states[i - 5]
            x = 1 - (i % 2)
        else:
            r = rng.random()
            if r < 0.2:
                y = 0
            elif r < 0.4:
                y = 1
            elif r < 0.6:
                y = 2
            elif r < 0.8:
                y = 3
            else:
                y = 4
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
