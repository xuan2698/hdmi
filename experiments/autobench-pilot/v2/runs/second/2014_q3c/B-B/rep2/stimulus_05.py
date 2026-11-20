def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i == 0:
            y = 0
            x = 0
        elif i == 1:
            y = 0
            x = 1
        elif i == 2:
            y = 1
            x = 0
        elif i == 3:
            y = 1
            x = 1
        elif i == 4:
            y = 2
            x = 0
        elif i == 5:
            y = 2
            x = 1
        elif i == 6:
            y = 3
            x = 0
        elif i == 7:
            y = 3
            x = 1
        elif i == 8:
            y = 4
            x = 0
        elif i == 9:
            y = 4
            x = 1
        else:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
