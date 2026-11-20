def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < 10:
            y = states[i % len(states)]
            x = i % 2
        elif i < 20:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        else:
            y = rng.randrange(8)
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
