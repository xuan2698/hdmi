def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i % 7 == 0:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        elif i % 7 == 1:
            y = 0
            x = 0
        elif i % 7 == 2:
            y = 0
            x = 1
        elif i % 7 == 3:
            y = 3
            x = rng.getrandbits(1)
        elif i % 7 == 4:
            y = 4
            x = rng.getrandbits(1)
        elif i % 7 == 5:
            y = rng.randrange(5)
            x = 1
        else:
            y = rng.randrange(5)
            x = 0
        seq.append({'x': x, 'y': y})
    return seq
