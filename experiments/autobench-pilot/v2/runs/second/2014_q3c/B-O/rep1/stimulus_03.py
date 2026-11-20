def Y0(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 0 and y0 == 0:
        return x
    if y2 == 0 and y1 == 0 and y0 == 1:
        return 0
    if y2 == 0 and y1 == 1 and y0 == 0:
        return 0
    if y2 == 0 and y1 == 1 and y0 == 1:
        return 0
    if y2 == 1 and y1 == 0 and y0 == 0:
        return 1
    return 0


def z(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 1 and y0 == 1:
        return 1
    if y2 == 1 and y1 == 0 and y0 == 0:
        return 1
    return 0


def stimulus(rng, cycles):
    seq = []
    states = [0, 1, 2, 3, 4]
    for i in range(cycles):
        if i % 7 == 0:
            y = 0
            x = 0
        elif i % 7 == 1:
            y = 0
            x = 1
        elif i % 7 == 2:
            y = 1
            x = 0
        elif i % 7 == 3:
            y = 3
            x = 1
        elif i % 7 == 4:
            y = 4
            x = 0
        elif i % 7 == 5:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        else:
            y = rng.randrange(5)
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
