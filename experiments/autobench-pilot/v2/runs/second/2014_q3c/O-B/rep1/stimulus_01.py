def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < 5:
            y = states[i]
            x = rng.getrandbits(1)
        elif i < 10:
            y = rng.choice(states)
            x = i % 2
        else:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
