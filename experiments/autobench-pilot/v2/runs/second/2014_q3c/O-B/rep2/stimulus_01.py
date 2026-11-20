def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i < 5:
            y = states[i]
            x = i & 1
        elif i < 10:
            y = states[(i - 5) % 5]
            x = (i + 1) & 1
        else:
            r = rng.randrange(10)
            if r < 3:
                y = rng.choice(states)
                x = rng.getrandbits(1)
            elif r < 6:
                y = rng.choice([0, 1, 3, 4])
                x = 1
            elif r < 8:
                y = rng.choice([0, 1, 2, 3])
                x = 0
            else:
                y = rng.randrange(5)
                x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
