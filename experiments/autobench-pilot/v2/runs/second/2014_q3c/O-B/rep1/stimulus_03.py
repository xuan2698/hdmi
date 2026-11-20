def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i % 7 == 0:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        elif i % 7 == 1:
            y = 3
            x = rng.getrandbits(1)
        elif i % 7 == 2:
            y = 4
            x = rng.getrandbits(1)
        elif i % 7 == 3:
            y = rng.choice([0, 1, 2])
            x = 1
        elif i % 7 == 4:
            y = rng.choice([0, 1, 2])
            x = 0
        elif i % 7 == 5:
            y = rng.randrange(8)
            x = rng.getrandbits(1)
        else:
            y = rng.choice(states)
            x = rng.choice([0, 1])
        seq.append({'x': x & 1, 'y': y & 7})
    return seq
