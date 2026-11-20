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
        if i < 5:
            y = states[i]
            x = i & 1
        elif i < 10:
            y = states[(i - 5) % 5]
            x = (i + 1) & 1
        else:
            y = rng.choice(states)
            x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
    return seq
