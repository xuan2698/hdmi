def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < len(states):
            y = states[i]
        else:
            r = rng.random()
            if r < 0.15:
                y = 0
            elif r < 0.3:
                y = 4
            elif r < 0.5:
                y = rng.choice(states)
            else:
                y = rng.randrange(8)
        x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
