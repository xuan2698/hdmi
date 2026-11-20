def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < 5:
            y = states[i]
            x = 0
        elif i < 10:
            y = states[i - 5]
            x = 1
        else:
            r = rng.randrange(10)
            if r < 3:
                y = rng.choice(states)
                x = 0
            elif r < 6:
                y = rng.choice(states)
                x = 1
            elif r < 8:
                y = rng.randrange(8)
                x = rng.getrandbits(1)
            else:
                y = rng.choice([0, 1, 3, 4])
                x = rng.getrandbits(1)
        seq.append({'x': x & 1, 'y': y & 7})
    return seq
