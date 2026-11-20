def Y0(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 0 and y0 == 0:
        return x
    if y2 == 0 and y1 == 0 and y0 == 1:
        return 0
    if y2 == 0 and y1 == 1 and y0 == 0:
        return x
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
    y = 0
    for i in range(cycles):
        if i % 7 == 0:
            y = 0
        x = rng.getrandbits(1)
        seq.append({'x': x, 'y': y})
        Y = 0
        if Y0(x, y):
            Y |= 1
        if y2_next(x, y):
            Y |= 4
        if y1_next(x, y):
            Y |= 2
        y = Y
    return seq

def y1_next(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 0 and y0 == 0:
        return 0
    if y2 == 0 and y1 == 0 and y0 == 1:
        return 0
    if y2 == 0 and y1 == 1 and y0 == 0:
        return 1
    if y2 == 0 and y1 == 1 and y0 == 1:
        return 1
    if y2 == 1 and y1 == 0 and y0 == 0:
        return 0
    return 0

def y2_next(x, y):
    y2 = (y >> 2) & 1
    y1 = (y >> 1) & 1
    y0 = y & 1
    if y2 == 0 and y1 == 0 and y0 == 0:
        return 0
    if y2 == 0 and y1 == 0 and y0 == 1:
        return 1
    if y2 == 0 and y1 == 1 and y0 == 0:
        return 0
    if y2 == 0 and y1 == 1 and y0 == 1:
        return 0
    if y2 == 1 and y1 == 0 and y0 == 0:
        return 1
    return 0
